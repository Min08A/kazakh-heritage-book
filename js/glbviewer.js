/**
 * Small dependency-free WebGL viewer for the simplified .glb models made for this project.
 * Supports: binary glTF 2.0, triangle meshes with POSITION + NORMAL, pbrMetallicRoughness colours.
 * Controls: drag = rotate, wheel / pinch = zoom, double-click = reset. No AR / WebXR.
 */

const COMP = { 5120: Int8Array, 5121: Uint8Array, 5122: Int16Array, 5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array };
const NCOMP = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 };

function parseGlb(buf) {
  const dv = new DataView(buf);
  if (dv.getUint32(0, true) !== 0x46546c67) throw new Error('Not a GLB file');
  let off = 12;
  let json = null;
  let bin = null;
  while (off < buf.byteLength) {
    const len = dv.getUint32(off, true);
    const type = dv.getUint32(off + 4, true);
    const data = buf.slice(off + 8, off + 8 + len);
    if (type === 0x4e4f534a) json = JSON.parse(new TextDecoder().decode(data));
    else if (type === 0x004e4942 && !bin) bin = data;
    off += 8 + len;
  }
  if (!json || !bin) throw new Error('Incomplete GLB file');
  const read = (idx) => {
    const a = json.accessors[idx];
    const v = json.bufferViews[a.bufferView];
    const C = COMP[a.componentType];
    const n = NCOMP[a.type];
    const start = (v.byteOffset || 0) + (a.byteOffset || 0);
    const stride = v.byteStride;
    if (stride && stride !== n * C.BYTES_PER_ELEMENT) {
      const out = new C(a.count * n);
      const src = new DataView(bin);
      for (let i = 0; i < a.count; i++) for (let k = 0; k < n; k++) {
        const p = start + i * stride + k * C.BYTES_PER_ELEMENT;
        out[i * n + k] = C === Float32Array ? src.getFloat32(p, true) : C === Uint16Array ? src.getUint16(p, true) : src.getUint32(p, true);
      }
      return out;
    }
    return new C(bin, start, a.count * n);
  };
  const prims = [];
  for (const node of json.nodes || []) {
    if (node.mesh == null) continue;
    for (const p of json.meshes[node.mesh].primitives) {
      if (p.mode != null && p.mode !== 4) continue;
      const mat = (json.materials && json.materials[p.material]) || {};
      const pbr = mat.pbrMetallicRoughness || {};
      prims.push({
        pos: read(p.attributes.POSITION),
        nor: p.attributes.NORMAL != null ? read(p.attributes.NORMAL) : null,
        idx: p.indices != null ? read(p.indices) : null,
        color: pbr.baseColorFactor || [0.8, 0.8, 0.8, 1],
        metal: pbr.metallicFactor ?? 1,
        rough: pbr.roughnessFactor ?? 1,
        double: !!mat.doubleSided,
      });
    }
  }
  if (!prims.length) throw new Error('No meshes found');
  return prims;
}

/* ---- tiny matrix helpers (column-major) ---- */
const mul = (a, b) => {
  const o = new Float32Array(16);
  for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
    let s = 0;
    for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k];
    o[c * 4 + r] = s;
  }
  return o;
};
const perspective = (fov, asp, n, f) => {
  const t = 1 / Math.tan(fov / 2);
  return new Float32Array([t / asp, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) / (n - f), -1, 0, 0, (2 * f * n) / (n - f), 0]);
};
const norm3 = (v) => { const l = Math.hypot(...v) || 1; return v.map((x) => x / l); };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const lookAt = (eye, ctr, up) => {
  const f = norm3([ctr[0] - eye[0], ctr[1] - eye[1], ctr[2] - eye[2]]);
  const s = norm3(cross(f, up));
  const u = cross(s, f);
  return new Float32Array([
    s[0], u[0], -f[0], 0, s[1], u[1], -f[1], 0, s[2], u[2], -f[2], 0,
    -(s[0] * eye[0] + s[1] * eye[1] + s[2] * eye[2]), -(u[0] * eye[0] + u[1] * eye[1] + u[2] * eye[2]), f[0] * eye[0] + f[1] * eye[1] + f[2] * eye[2], 1,
  ]);
};

const VS = `
attribute vec3 aPos; attribute vec3 aNor;
uniform mat4 uProj; uniform mat4 uView; uniform mat4 uModel;
varying vec3 vN; varying vec3 vP;
void main(){
  vec4 p = uView * uModel * vec4(aPos, 1.0);
  vP = p.xyz;
  vN = mat3(uView) * aNor;
  gl_Position = uProj * p;
}`;

const FS = `
precision mediump float;
varying vec3 vN; varying vec3 vP;
uniform vec3 uBase; uniform float uMetal; uniform float uRough; uniform float uDouble;
void main(){
  vec3 N = normalize(vN);
  if (uDouble > 0.5 && !gl_FrontFacing) N = -N;
  vec3 V = normalize(-vP);
  vec3 L1 = normalize(vec3(-0.45, 0.75, 0.65));
  vec3 L2 = normalize(vec3(0.75, 0.15, 0.35));
  float d1 = max(dot(N, L1), 0.0);
  float d2 = max(dot(N, L2), 0.0);
  vec3 hemi = mix(vec3(0.20, 0.17, 0.14), vec3(0.62, 0.66, 0.72), N.y * 0.5 + 0.5);
  vec3 diff = uBase * (1.0 - uMetal * 0.8);
  vec3 H = normalize(L1 + V);
  float shin = mix(90.0, 8.0, uRough);
  float spec = pow(max(dot(N, H), 0.0), shin) * (1.0 - uRough * 0.75);
  vec3 specCol = mix(vec3(0.22), uBase, uMetal);
  vec3 R = reflect(-V, N);
  vec3 env = mix(vec3(0.20, 0.17, 0.15), vec3(0.95, 0.96, 1.0), clamp(R.y * 0.5 + 0.5, 0.0, 1.0));
  vec3 col = diff * (hemi * 0.95 + d1 * vec3(1.0, 0.95, 0.88) * 0.8 + d2 * vec3(0.7, 0.85, 1.0) * 0.28);
  col += specCol * spec * 0.9;
  col += uMetal * uBase * env * 0.5 * (1.0 - uRough * 0.45);
  col = pow(col, vec3(1.0 / 2.2));
  gl_FragColor = vec4(col, 1.0);
}`;

function compile(gl, type, src) {
  const s = gl.createShader(type);
  gl.shaderSource(s, src);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) || 'shader error');
  return s;
}

/**
 * Mounts the viewer inside `container`. Resolves with { reset, setAutoRotate, destroy }.
 * Rejects when WebGL is not available or the file cannot be loaded/parsed.
 */
export async function mountGlbViewer(container, url, { alt = '3D model' } = {}) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const prims = parseGlb(await res.arrayBuffer());

  const canvas = document.createElement('canvas');
  canvas.className = 'glb-canvas';
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', `${alt}. Drag to rotate, scroll or pinch to zoom.`);
  canvas.tabIndex = 0;
  const gl = canvas.getContext('webgl', { antialias: true, alpha: true, premultipliedAlpha: true });
  if (!gl) throw new Error('WebGL is not available');

  const prog = gl.createProgram();
  gl.attachShader(prog, compile(gl, gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, compile(gl, gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error('shader link failed');
  gl.useProgram(prog);
  const loc = (n) => gl.getUniformLocation(prog, n);
  const U = { proj: loc('uProj'), view: loc('uView'), model: loc('uModel'), base: loc('uBase'), metal: loc('uMetal'), rough: loc('uRough'), dbl: loc('uDouble') };
  const aPos = gl.getAttribLocation(prog, 'aPos');
  const aNor = gl.getAttribLocation(prog, 'aNor');
  const uint = gl.getExtension('OES_element_index_uint');

  // bounds
  const mn = [Infinity, Infinity, Infinity];
  const mx = [-Infinity, -Infinity, -Infinity];
  for (const p of prims) for (let i = 0; i < p.pos.length; i += 3) for (let k = 0; k < 3; k++) {
    mn[k] = Math.min(mn[k], p.pos[i + k]);
    mx[k] = Math.max(mx[k], p.pos[i + k]);
  }
  const ctr = mn.map((v, k) => (v + mx[k]) / 2);
  const radius = Math.max(Math.hypot(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]) / 2, 1e-6);
  const s = 1 / radius;
  const model = new Float32Array([s, 0, 0, 0, 0, s, 0, 0, 0, 0, s, 0, -ctr[0] * s, -ctr[1] * s, -ctr[2] * s, 1]);

  const buffers = prims.map((p) => {
    const pb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pb);
    gl.bufferData(gl.ARRAY_BUFFER, p.pos, gl.STATIC_DRAW);
    const nb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nb);
    gl.bufferData(gl.ARRAY_BUFFER, p.nor || new Float32Array(p.pos.length), gl.STATIC_DRAW);
    let idx = p.idx;
    let count;
    let type = gl.UNSIGNED_SHORT;
    if (!idx) {
      count = p.pos.length / 3;
      idx = count < 65536 ? Uint16Array.from({ length: count }, (_, i) => i) : Uint32Array.from({ length: count }, (_, i) => i);
    } else count = idx.length;
    if (idx instanceof Uint32Array) {
      if (p.pos.length / 3 < 65536) idx = Uint16Array.from(idx);
      else if (uint) type = gl.UNSIGNED_INT;
      else throw new Error('Mesh too large for this device');
    }
    const ib = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, idx, gl.STATIC_DRAW);
    const lin = p.color;
    return { pb, nb, ib, count, type, color: [lin[0], lin[1], lin[2]], metal: p.metal, rough: p.rough, dbl: p.double ? 1 : 0 };
  });

  container.replaceChildren(canvas);

  const home = { yaw: 0.6, pitch: 0.28, dist: 3.7 };
  const cam = { ...home };
  let auto = true;
  let userTouched = false;
  let dirty = true;
  let alive = true;
  let last = performance.now();

  function resize() {
    const r = container.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.round(r.width * dpr));
    const h = Math.max(1, Math.round(r.height * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    dirty = true;
  }
  const ro = new ResizeObserver(resize);
  ro.observe(container);
  resize();

  function draw(now) {
    if (!alive) return;
    if (!canvas.isConnected) {
      requestAnimationFrame(draw);
      return;
    }
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (auto && !userTouched) {
      cam.yaw += dt * 0.35;
      dirty = true;
    }
    if (dirty) {
      dirty = false;
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clearColor(0, 0, 0, 0);
      gl.enable(gl.DEPTH_TEST);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      const eye = [
        cam.dist * Math.cos(cam.pitch) * Math.sin(cam.yaw),
        cam.dist * Math.sin(cam.pitch),
        cam.dist * Math.cos(cam.pitch) * Math.cos(cam.yaw),
      ];
      gl.uniformMatrix4fv(U.proj, false, perspective(0.6, canvas.width / canvas.height, 0.1, 50));
      gl.uniformMatrix4fv(U.view, false, lookAt(eye, [0, 0, 0], [0, 1, 0]));
      gl.uniformMatrix4fv(U.model, false, model);
      for (const b of buffers) {
        gl.bindBuffer(gl.ARRAY_BUFFER, b.pb);
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, b.nb);
        gl.enableVertexAttribArray(aNor);
        gl.vertexAttribPointer(aNor, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, b.ib);
        gl.uniform3f(U.base, b.color[0], b.color[1], b.color[2]);
        gl.uniform1f(U.metal, b.metal);
        gl.uniform1f(U.rough, b.rough);
        gl.uniform1f(U.dbl, b.dbl);
        gl.drawElements(gl.TRIANGLES, b.count, b.type, 0);
      }
    }
    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);

  /* ---- pointer controls ---- */
  const pts = new Map();
  let pinch = 0;
  canvas.style.touchAction = 'none';
  canvas.addEventListener('pointerdown', (e) => {
    canvas.setPointerCapture(e.pointerId);
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    userTouched = true;
    if (pts.size === 2) {
      const [a, b] = [...pts.values()];
      pinch = Math.hypot(a.x - b.x, a.y - b.y);
    }
  });
  canvas.addEventListener('pointermove', (e) => {
    const p = pts.get(e.pointerId);
    if (!p) return;
    const dx = e.clientX - p.x;
    const dy = e.clientY - p.y;
    p.x = e.clientX;
    p.y = e.clientY;
    if (pts.size === 1) {
      cam.yaw -= dx * 0.008;
      cam.pitch = Math.max(-1.35, Math.min(1.35, cam.pitch + dy * 0.008));
    } else if (pts.size === 2) {
      const [a, b] = [...pts.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (pinch) cam.dist = Math.max(1.8, Math.min(8, cam.dist * (pinch / d)));
      pinch = d;
    }
    dirty = true;
  });
  const up = (e) => {
    pts.delete(e.pointerId);
    pinch = 0;
  };
  canvas.addEventListener('pointerup', up);
  canvas.addEventListener('pointercancel', up);
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    cam.dist = Math.max(1.8, Math.min(8, cam.dist * Math.exp(e.deltaY * 0.001)));
    userTouched = true;
    dirty = true;
  }, { passive: false });
  const reset = () => {
    Object.assign(cam, home);
    userTouched = false;
    dirty = true;
  };
  canvas.addEventListener('dblclick', reset);
  canvas.addEventListener('keydown', (e) => {
    const k = { ArrowLeft: [-0.12, 0], ArrowRight: [0.12, 0], ArrowUp: [0, -0.1], ArrowDown: [0, 0.1] }[e.key];
    if (k) {
      e.preventDefault();
      userTouched = true;
      cam.yaw += k[0];
      cam.pitch = Math.max(-1.35, Math.min(1.35, cam.pitch + k[1]));
      dirty = true;
    } else if (e.key === '+' || e.key === '=') { cam.dist = Math.max(1.8, cam.dist * 0.9); dirty = true; }
    else if (e.key === '-') { cam.dist = Math.min(8, cam.dist * 1.1); dirty = true; }
  });
  canvas.addEventListener('webglcontextlost', (e) => e.preventDefault());

  return {
    reset,
    setAutoRotate(v) { auto = v; userTouched = !v; dirty = true; },
    destroy() {
      alive = false;
      ro.disconnect();
      canvas.remove();
    },
  };
}
