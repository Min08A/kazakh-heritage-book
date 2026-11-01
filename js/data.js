/**
 * All chapter content lives here. Edit text, models and credits in this file only.
 *
 * model.sketchfab  – a Sketchfab model that was checked on its model page (title, creator, embed button).
 * model.glb        – a simplified 3D model generated for this project (tools/make_models.py), used when
 *                    there is no usable Sketchfab model, or as a fallback if the Sketchfab embed fails.
 * Media: media/videos/<slug>.mp4 + .webm, media/images/<slug>.jpg, optional media/audio/<slug>.mp3.
 */

const SF = 'https://sketchfab.com';
const GENERATED = 'Simplified model generated for this project (no third-party assets).';

export const objects = [
  {
    slug: 'dombra',
    n: 1,
    title: 'Dombra',
    native: 'Домбыра',
    subtitle: 'The two-string voice of the steppe',
    summary: 'A long-necked, two-string instrument at the heart of Kazakh music.',
    description:
      'The dombra is the best-loved instrument of the Kazakh people. Its small wooden body is attached to a long, slender neck, and two strings stretch along its length. Players strum or strike the strings with the right hand in quick, rhythmic patterns, while the left hand presses them against the frets to shape the melody. The dombra accompanies the songs of the akyns, the traditional poet-singers, and carries the kuy, short instrumental pieces that tell stories of nature, history and feeling. For generations it has been a companion at feasts, gatherings and quiet evenings, and a living voice of Kazakh memory.',
    facts: [
      'A kuy is a short instrumental composition, often inspired by a legend, a landscape or an event.',
      'Akyns are poet-singers who improvise verse, often accompanied by the dombra.',
      'In Kazakh families the dombra is traditionally treated with great respect.',
    ],
    transcript:
      'Welcome to the world of the dombra. This is the most beloved instrument of the Kazakh people. Look closely at its shape: a small wooden body, a long and slender neck, and just two strings. Yet from these two strings, a musician can draw thunder, galloping horses, rippling water and gentle lullabies. The player strums the strings with the right hand and shapes the melody with the left, pressing along the frets. The dombra is the voice of the akyn, the poet-singer, who answers a rival in verse. It also carries the kuy, a short piece of instrumental music that tells a story without words. Turn the model, zoom in on the neck and the body, and imagine this instrument in the hands of a singer, at a feast, under the wide Kazakh sky.',
    model: {
      sketchfab: {
        uid: 'c75f815bb74f426a9d923642c52f8f9a',
        url: `${SF}/3d-models/kazakh-dombra-c75f815bb74f426a9d923642c52f8f9a`,
        title: 'Kazakh Dombra',
        creator: 'Q3D_Library',
        creatorUrl: `${SF}/Q3D_Open_Library`,
        license: 'CC Attribution 4.0',
      },
      glb: { src: 'models/dombra.glb', alt: 'Simplified 3D model of a Kazakh dombra', note: GENERATED },
    },
  },
  {
    slug: 'yurt',
    n: 2,
    title: 'Kazakh Yurt',
    native: 'Киіз үй',
    subtitle: 'The portable home of the nomads',
    summary: 'A felt-covered dwelling built to travel with the seasons.',
    description:
      'The Kazakh yurt, called kiyiz uy, or "felt house", is the portable home of the steppe. Its frame is built from kerege, folding lattice walls of willow, joined by uyk, long roof poles that rise like the ribs of an umbrella to meet in the shanyrak, the wooden ring at the crown. Thick felt covers the frame, keeping the interior warm in winter and cool in summer. A family could take a yurt down and raise it again within hours, moving with the seasons between pastures. The shanyrak, which lets in light and releases smoke, is a symbol of home and family.',
    facts: [
      'The kerege are the folding lattice walls; the uyk are the roof poles; the shanyrak is the crown ring.',
      'The shanyrak is a symbol of the family home and is often handed down through generations.',
      'Felt coverings can be added or removed to adapt the yurt to the weather.',
    ],
    transcript:
      'Step inside the Kazakh yurt, the kiyiz uy, which means the felt house. For centuries, nomadic families carried their homes across the steppe, and this is how they did it. The walls are the kerege, folding lattices of willow that open and close like an accordion. Long poles, the uyk, rise from the walls like the ribs of an umbrella, and they meet at the top in a great wooden ring, the shanyrak. Thick felt wraps the frame, warm in winter and cool in summer. When the season changed, the family would take the yurt down and raise it again in a new place within hours. The shanyrak is more than a roof opening. It is a symbol of the home itself, a sign of family, continuity and belonging.',
    model: {
      sketchfab: {
        uid: 'e1c2aab9945c455d914b3ac6e4095dee',
        url: `${SF}/3d-models/kasakh-yurta-e1c2aab9945c455d914b3ac6e4095dee`,
        title: 'Kasakh Yurta. Казахская юрта.',
        creator: 'Valger',
        creatorUrl: `${SF}/Valger`,
        license: null,
        note: 'The model page does not state a license. Confirm the terms with the creator before a public launch.',
      },
      glb: { src: 'models/yurt.glb', alt: 'Simplified 3D model of a Kazakh yurt', note: GENERATED },
    },
  },
  {
    slug: 'kobyz',
    n: 3,
    title: 'Kobyz',
    native: 'Қобыз',
    subtitle: 'The ancient bowed instrument',
    summary: 'A horsehair-stringed fiddle with a deep, haunting voice.',
    description:
      'The kobyz is an ancient bowed instrument of the Kazakh steppe. Its body is hollowed from wood and joined to a long neck, and it carries two strings made of horsehair. A bow, also strung with horsehair, is drawn across the strings while the player holds the instrument upright. Its low, husky, haunting voice was long associated with the baqsy, healers and shamans who played to ease suffering and guide spirits. Today the kobyz is remembered through the legend of Korkyt Ata, the sage and musician of Turkic tradition, and its music is performed on concert stages, keeping an ancient sound alive.',
    facts: [
      'The kobyz is a bowed instrument, unlike the plucked dombra.',
      'Its strings and bow are traditionally made of horsehair.',
      'Korkyt Ata, a legendary sage, is closely associated with the kobyz in Turkic tradition.',
    ],
    transcript:
      'This is the kobyz, one of the oldest instruments of the Kazakh steppe. Unlike the dombra, which is plucked, the kobyz is played with a bow. Both the bow and the two strings are traditionally made of horsehair, which gives the instrument its low, husky and slightly mysterious voice. The player holds the kobyz upright and draws the bow across the strings. In older times, the music of the kobyz was linked with the baqsy, healers who played to calm the sick and to speak with the spirits. The instrument is also tied to the legend of Korkyt Ata, a wise musician who, the stories say, played to push back death itself. Rotate the model and look at the hollowed body and the long neck. Listen with your imagination to a very old sound.',
    model: {
      sketchfab: {
        uid: 'c94229e78d834bd4bb465c287d7f01c1',
        url: `${SF}/3d-models/kazakh-qobyz-kobyz-c94229e78d834bd4bb465c287d7f01c1`,
        title: 'Kazakh Qobyz (Kobyz)',
        creator: 'Q3D_Library',
        creatorUrl: `${SF}/Q3D_Open_Library`,
        license: 'CC Attribution 4.0',
      },
      glb: { src: 'models/kobyz.glb', alt: 'Simplified 3D model of a Kazakh kobyz with its bow', note: GENERATED },
    },
  },
  {
    slug: 'saukele',
    n: 4,
    title: 'Saukele',
    native: 'Сәукеле',
    subtitle: 'The bride’s crowning headdress',
    summary: 'A tall, richly decorated headdress worn by the Kazakh bride.',
    description:
      'The saukele is the tall, conical headdress worn by a Kazakh bride on her wedding day. Its firm cone is covered with fine fabric and decorated with silver and gilded ornaments, coral, pearls and semiprecious stones. Long strands of beads and pendants frame the face, and a veil may fall over the shoulders. Making a saukele took months of careful work by skilled craftswomen, and a fine one could be treasured and passed down within a family. Beyond its beauty, the saukele expressed the status of the family and the good wishes of relatives for the happiness of the young bride.',
    facts: [
      'The saukele is worn at weddings and is one of the most elaborate pieces of Kazakh traditional dress.',
      'Silver, coral, pearls and semiprecious stones are common decorative materials.',
      'Fine examples were valued as family heirlooms.',
    ],
    transcript:
      'Here is the saukele, the headdress of a Kazakh bride. Notice how tall it rises, in an elegant cone. Imagine the bride on her wedding day, wearing this crown, the centre of everyone’s attention. The cone is covered with fine fabric and decorated with silver, gilded ornaments, coral, pearls and stones. Long strands of beads and pendants hang beside the face, catching the light with every movement. A saukele took months to make, with many skilled hands working on every detail. It was not only a beautiful ornament. It showed the pride of the family and carried the best wishes of relatives for the bride’s new life. Turn the model around, and look at the decorations from every side.',
    model: {
      sketchfab: {
        uid: 'f43d8846f6974133a238432d8e56a030',
        url: `${SF}/3d-models/saukele-traditional-kazakh-headwear-f43d8846f6974133a238432d8e56a030`,
        title: 'Saukele - Traditional Kazakh Headwear',
        creator: 'aibolat.visuals',
        creatorUrl: null,
        license: null,
        note: 'The model page does not state a license. Confirm the terms with the creator before a public launch.',
      },
      glb: { src: 'models/saukele.glb', alt: 'Simplified 3D model of a saukele bridal headdress', note: GENERATED },
    },
  },
  {
    slug: 'shapan',
    n: 5,
    title: 'Shapan',
    native: 'Шапан',
    subtitle: 'The robe of respect and welcome',
    summary: 'A long outer robe worn for warmth, festivity and honour.',
    description:
      'The shapan is the traditional Kazakh long outer robe, worn by both men and women. Made from wool, camel hair or heavy cotton and often lined, it protects against wind and cold on the open steppe. Festive versions are cut from velvet or silk and richly decorated with embroidery and braided trim along the edges. Presenting a shapan is a gesture of deep respect: it is traditionally offered to honoured guests, to a groom, or to an elder, and being given one is a sign of welcome and honour. Today the shapan still appears at celebrations and ceremonies.',
    facts: [
      'The shapan was worn by both men and women in different styles.',
      'Placing a shapan on a guest’s shoulders is a traditional gesture of honour.',
      'Festive shapans were embroidered or trimmed with braid.',
    ],
    transcript:
      'This is the shapan, the long robe of the Kazakh steppe. In the cold winds of the open country, a shapan kept its wearer warm. It was made of wool, camel hair or sturdy cotton, and often lined for extra protection. For celebrations, craftspeople made festive shapans from velvet or silk, with embroidery and braided trim along the edges. But the shapan is more than clothing. Placing a shapan on the shoulders of a guest, a groom or an elder is a gesture of deep respect. It says: you are welcome, and you are honoured. Today, the shapan still appears at weddings, ceremonies and national celebrations as a living symbol of hospitality.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=Kazakh%20shapan`,
      glb: { src: 'models/shapan.glb', alt: 'Simplified 3D model of a Kazakh shapan robe', note: GENERATED },
    },
  },
  {
    slug: 'beshbarmak',
    n: 6,
    title: 'Beshbarmak',
    native: 'Бесбармақ',
    subtitle: 'The dish of five fingers and shared tables',
    summary: 'The celebrated Kazakh meal of boiled meat and broad noodles.',
    description:
      'Beshbarmak, whose name means "five fingers", is the best-known dish of Kazakh hospitality. Nomads traditionally ate it with their hands. Pieces of boiled meat, such as horse, lamb or beef, are served over wide, thin sheets of boiled dough and topped with onions simmered in the broth. A bowl of the rich broth, called sorpa, is served alongside. At the table, the host shares the best cuts to honour the guests and elders. Prepared for weddings, holidays and family gatherings, beshbarmak is a meal about togetherness, generosity and welcoming those who arrive.',
    facts: [
      'The name beshbarmak means "five fingers", recalling how the dish was eaten by hand.',
      'The broth is served separately in bowls and is called sorpa.',
      'Serving the best cuts to guests and elders is a sign of respect.',
    ],
    transcript:
      'Welcome to the table. This is beshbarmak, whose name means five fingers, because the nomads traditionally ate it with their hands. Boiled meat, such as horse, lamb or beef, is laid over wide, thin sheets of dough. Onions, softened in the broth, are spread over the top. Alongside comes a bowl of hot broth called sorpa. Beshbarmak is not a quick meal. It is prepared for weddings, holidays and when honoured guests arrive. The host shares out the best pieces of meat to the elders and the guests, as a sign of respect. In Kazakh culture, the table is a place for generosity, for conversation and for being together.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=beshbarmak`,
      glb: { src: 'models/beshbarmak.glb', alt: 'Simplified 3D model of beshbarmak on a plate with a bowl of broth', note: GENERATED },
    },
  },
  {
    slug: 'besik',
    n: 7,
    title: 'Besik',
    native: 'Бесік',
    subtitle: 'The cradle that welcomes a child',
    summary: 'The carved wooden cradle at the heart of family tradition.',
    description:
      'The besik is the traditional wooden cradle of Kazakh families. Made from light wood such as birch, pine or willow, it was easy to carry when a family moved between pastures. Its rounded base lets it rock gently, and the baby is wrapped and secured with soft ribbons. A small opening with a drain tube kept the cradle hygienic. Many besiks are carved and decorated, and protective charms were often attached to guard the child. A besik could be inherited within the family, and the besik toi, a celebration for placing a baby in the cradle for the first time, welcomes a new life.',
    facts: [
      'Besiks are traditionally made from light woods such as birch, pine or willow.',
      'Protective charms were often attached to the cradle.',
      'The besik toi is a celebration held when a baby is first placed in the cradle.',
    ],
    transcript:
      'This is the besik, the traditional Kazakh cradle. Made from light wood such as birch, pine or willow, it was easy to carry from one pasture to the next. Its curved base lets the cradle rock gently, and the baby is wrapped snugly and tied with soft ribbons. Many besiks are carved with patterns, and families often added protective charms to keep the child safe. A besik could be passed from one generation to the next. When a baby is first laid in the cradle, the family holds a celebration called besik toi, welcoming the new life with songs, good wishes and a shared table. The besik reminds us that Kazakh heritage begins with family.',
    model: {
      sketchfab: {
        uid: '39d686c6f74b463d9633847b1d217ac6',
        url: `${SF}/3d-models/besik-39d686c6f74b463d9633847b1d217ac6`,
        title: 'Besik',
        creator: 'Adil77',
        creatorUrl: `${SF}/AdilAlmaty`,
        license: null,
        note: 'The model page does not state a license (its wording suggests a paid royalty-free model). Confirm the terms with the creator before a public launch.',
      },
      // Used automatically if the Sketchfab embed cannot be loaded.
      glb: { src: 'models/besik.glb', alt: 'Simplified 3D model of a Kazakh besik cradle', note: GENERATED },
    },
  },
  {
    slug: 'torsyk',
    n: 8,
    title: 'Torsyk',
    native: 'Торсық',
    subtitle: 'The leather vessel of the road',
    summary: 'A sewn leather flask made for carrying drinks across the steppe.',
    description:
      'The torsyk is a traditional leather vessel for carrying and storing drinks, especially kumys, the fermented mare’s milk beloved on the steppe. Craftsmen cut and sewed tanned hide into a rounded vessel with a narrow neck and handles, and often decorated it with embossed patterns. Light, durable and resistant to knocks, the torsyk suited a life on the move, when a rider needed to carry drink over long distances. The leather also helped keep the drink cool. Today the torsyk reminds us how ingeniously nomadic families made everyday objects from the materials of their herds.',
    facts: [
      'Kumys is fermented mare’s milk, a traditional drink of the steppe.',
      'Leather decoration included embossing with carved wooden plates.',
      'Leather vessels came in several shapes for different kinds of drink.',
    ],
    transcript:
      'This is the torsyk, a traditional Kazakh leather vessel. On the steppe, a rider might travel for days, and needed a way to carry a drink. The torsyk was the answer. Craftsmen cut and sewed tanned hide into a rounded vessel with a narrow neck and handles. It was often filled with kumys, the fermented mare’s milk that is a treasured drink of the steppe. The leather was light, tough and did not break when it was knocked. Many torsyks were decorated with embossed patterns pressed into the hide. The torsyk shows how nomadic families made clever, beautiful tools from the materials they had, the products of their own herds.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=Kazakh%20torsyk`,
      glb: { src: 'models/torsyk.glb', alt: 'Simplified 3D model of a Kazakh torsyk leather flask', note: GENERATED },
    },
  },
];

export const bySlug = (slug) => objects.find((o) => o.slug === slug) || null;
export const neighbours = (slug) => {
  const i = objects.findIndex((o) => o.slug === slug);
  return { prev: i > 0 ? objects[i - 1] : null, next: i >= 0 && i < objects.length - 1 ? objects[i + 1] : null };
};
export const videoSources = (o) => ({ mp4: `media/videos/${o.slug}.mp4`, webm: `media/videos/${o.slug}.webm` });
export const coverOf = (o) => `media/images/${o.slug}.jpg`;
export const audioUrlOf = (o) => `media/audio/${o.slug}.mp3`;
