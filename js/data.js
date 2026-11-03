/**
 * All chapter content lives here. Edit text, models and credits in this file only.
 *
 * The book has two parts (see `parts`). Chapters are listed in reading order; `n` (the chapter
 * number) is assigned automatically from that order, so reordering entries renumbers the book.
 *
 * model.sketchfab  – a Sketchfab model that was checked on its model page (title, creator, license).
 * model.glb        – a simplified 3D model generated for this project (tools/make_models*.py), used when
 *                    there is no usable Sketchfab model, or as a fallback if the Sketchfab embed fails.
 * Media: media/videos/<slug>.mp4, media/images/<slug>.jpg, optional media/audio/<slug>.mp3.
 * `transcript` is the text shown under the narration player (and read aloud by the browser voice
 * when there is no audio file).
 */

const SF = 'https://sketchfab.com';
const GENERATED = 'Simplified model generated for this project (no third-party assets).';
const NO_LICENSE = 'The model page does not state a license. Confirm the terms with the creator before a public launch.';
const sfUrl = (uid) => `${SF}/3d-models/${uid}`;
const glb = (slug, alt) => ({ src: `models/${slug}.glb`, alt, note: GENERATED });

export const parts = [
  { id: 1, label: 'Part 1', title: 'Textbook Vocabulary', native: 'Оқулық сөздігі', intro: 'Six words from the textbook: famous places, a legend, the home of the nomads and an everyday drink.' },
  { id: 2, label: 'Part 2', title: 'Proposed Vocabulary', native: 'Ұсынылған сөздік', intro: 'More words from life on the steppe: games and contests, food and drink, crafts, journeys and the seasons of nomadic life.' },
];

const list = [
  /* ============================================================== PART 1 */
  {
    slug: 'khan-shatyr',
    part: 1,
    title: 'Khan Shatyr',
    native: 'Хан Шатыр',
    transcription: 'han shatır',
    topic:
      'On a freezing winter day, families in Astana stroll through [[Khan Shatyr]] in light clothes, because the transparent tent keeps the air inside warm.',
    subtitle: 'The royal tent of Astana',
    summary: 'A giant transparent tent that shelters a whole town of shops, parks and a beach.',
    description:
      'Khan Shatyr, whose name means "the khan’s tent", is one of the best-known buildings of Astana. It was designed by the British architect Norman Foster and opened in 2010. Its shape recalls a nomadic tent: a tall steel mast rises in the middle, and a net of cables holds a light, transparent roof that lets the daylight in. Under this roof, the air stays warm even in the freezing Astana winter. Inside there are shops, cafés, a park with paths and even an indoor beach. Khan Shatyr shows how the image of the old nomadic tent can inspire modern architecture.',
    facts: [
      'The name Khan Shatyr means "the khan’s tent" or "royal tent".',
      'The building was designed by Foster + Partners and opened in 2010.',
      'Its transparent roof keeps a warm climate inside, even when it is very cold outside.',
    ],
    transcript:
      'Khan Shatyr means the khan’s tent. This giant transparent tent in Astana shelters shops, cafés, a park and even a beach, and its shape recalls the tents of the nomads.',
    model: {
      sketchfab: {
        uid: 'd046e2a88ec64c1fa9561900f52e7a03',
        url: `${SF}/3d-models/khan-shatyr-d046e2a88ec64c1fa9561900f52e7a03`,
        title: 'Khan Shatyr / Хан Шатыр',
        creator: 'droneskz',
        creatorUrl: `${SF}/droneskz`,
        license: null,
        note: NO_LICENSE,
      },
      glb: glb('khan-shatyr', 'Simplified 3D model of the Khan Shatyr tent building'),
    },
  },
  {
    slug: 'yurt',
    part: 1,
    title: 'Kiiz Ui',
    native: 'Киіз үй',
    transcription: 'kiíz üy',
    topic:
      'As a guest, you enter the [[kiiz ui]] and sit at a round low table. Colourful hand-crafted rugs and blankets cover the floor and walls, and the felt protects the family from the weather.',
    subtitle: 'The portable home of the nomads',
    summary: 'The felt-covered yurt, built to travel with the seasons.',
    description:
      'The Kazakh yurt, called kiiz ui, or "felt house", is the portable home of the steppe. Its frame is built from kerege, folding lattice walls of willow, joined by uyk, long roof poles that rise like the ribs of an umbrella to meet in the shanyraq, the wooden ring at the crown. Thick felt covers the frame, keeping the interior warm in winter and cool in summer. A family could take a yurt down and raise it again within hours, moving with the seasons between pastures. The shanyraq, which lets in light and releases smoke, is a symbol of home and family.',
    facts: [
      'The kerege are the folding lattice walls; the uyk are the roof poles; the shanyraq is the crown ring.',
      'The shanyraq is a symbol of the family home and is often handed down through generations.',
      'Felt coverings can be added or removed to adapt the yurt to the weather.',
    ],
    transcript:
      'Kiiz ui, the felt house, is the Kazakh yurt. Lattice walls, curved roof poles and a crown ring are covered with thick felt, and a family can take it down and raise it again within hours.',
    model: {
      sketchfab: {
        uid: 'e1c2aab9945c455d914b3ac6e4095dee',
        url: `${SF}/3d-models/kasakh-yurta-e1c2aab9945c455d914b3ac6e4095dee`,
        title: 'Kasakh Yurta. Казахская юрта.',
        creator: 'Valger',
        creatorUrl: `${SF}/Valger`,
        license: null,
        note: NO_LICENSE,
      },
      glb: glb('yurt', 'Simplified 3D model of a Kazakh yurt'),
    },
  },
  {
    slug: 'kyz-zhibek',
    part: 1,
    title: 'Kyz Zhibek',
    native: 'Қыз Жібек',
    transcription: 'qız zhíbek',
    topic:
      'At a festival, an akyn sings the story of [[Kyz Zhibek]] to the dombra, and the audience listens to the tale of love and loyalty.',
    subtitle: 'The silk maiden of the great love epic',
    summary: 'The heroine of a famous Kazakh love story, told in verse, on stage and on screen.',
    description:
      'Kyz Zhibek, "the silk maiden", is the heroine of one of the best-loved Kazakh lyric epics. The poem tells of the young hero Tolegen, who travels far across the steppe to find the beautiful Zhibek. The two fall in love, but jealousy and rivalry lead to tragedy: Tolegen is killed on his way back to his bride. The story is told in verse by akyns and zhyraus and has been passed down from generation to generation. In the twentieth century it became the first Kazakh opera, with a libretto by the writer Gabit Musirepov, and later a much-loved film. Zhibek is remembered for her beauty, loyalty and courage.',
    facts: [
      'Zhibek means "silk", a word that praises her beauty and grace.',
      'The opera "Kyz Zhibek", with a libretto by Gabit Musirepov, is considered the first Kazakh opera.',
      'Girls in the epic wear a takiya, a cap often decorated with owl feathers, embroidery and beads.',
    ],
    transcript:
      'Kyz Zhibek, the silk maiden, is the heroine of a famous Kazakh love epic. Her story with the hero Tolegen is told in verse, and it became the first Kazakh opera and a much-loved film.',
    model: {
      sketchfab: {
        uid: '78a402f6ac3d41bd9c8f581b39a5345e',
        url: sfUrl('78a402f6ac3d41bd9c8f581b39a5345e'),
        title: 'Taqiya Yellow (F) (Kazakh Traditional Headdress)',
        creator: 'Q3D_Library',
        creatorUrl: `${SF}/Q3D_Open_Library`,
        license: 'CC Attribution 4.0',
        about: 'A girl’s takiya, the kind of cap worn by young women like Zhibek.',
      },
      glb: glb('kyz-zhibek', 'Simplified 3D model of a girl’s takiya cap with feathers'),
    },
  },
  {
    slug: 'aisha-bibi',
    part: 1,
    title: 'Aisha Bibi',
    native: 'Айша бибі',
    transcription: 'aysha bíbí',
    topic:
      'Young couples visiting Taraz stop at [[Aisha Bibi]] to admire the carved tiles and hear the legend of faithful love.',
    subtitle: 'A monument to faithful love',
    summary: 'A medieval mausoleum near Taraz, covered with carved terracotta patterns.',
    description:
      'The mausoleum of Aisha Bibi stands near the city of Taraz, in the village that bears her name. It was built in the eleventh or twelfth century and is famous for its walls of carved terracotta tiles, covered with dozens of different geometric and plant patterns. Legend says that Aisha, the daughter of a learned man, loved Karakhan, the ruler of Taraz. On her way to marry him she was bitten by a snake and died. In his grief, Karakhan built this beautiful mausoleum over her grave. Today it is a protected monument of Kazakh history, and young couples visit it as a symbol of faithful love.',
    facts: [
      'Its walls are covered with carved terracotta tiles in many different patterns.',
      'Nearby stands the mausoleum of Babaji Khatun, said to be Aisha’s nanny.',
      'The legend of Aisha Bibi is linked with Karakhan, whose mausoleum stands in Taraz.',
    ],
    transcript:
      'Aisha Bibi is a medieval mausoleum near Taraz, covered with carved terracotta patterns. Legend says that Karakhan built it in memory of his beloved Aisha.',
    model: {
      sketchfab: {
        uid: '9607c288202740ac90879f05076d06ce',
        url: `${SF}/3d-models/the-mausoleum-of-aisha-bibi-9607c288202740ac90879f05076d06ce`,
        title: 'The mausoleum of Aisha Bibi',
        creator: 'Askhat Shulenbay',
        creatorUrl: `${SF}/shulenbay`,
        license: null,
        note: NO_LICENSE,
      },
      glb: glb('aisha-bibi', 'Simplified 3D model of the Aisha Bibi mausoleum'),
    },
  },
  {
    slug: 'karakhan',
    part: 1,
    title: 'Karakhan',
    native: 'Қарахан',
    transcription: 'qarahan',
    topic:
      'In Taraz, guides tell how the ruler [[Karakhan]] built a mausoleum in memory of his beloved Aisha.',
    subtitle: 'The mausoleum of the holy ruler of Taraz',
    summary: 'The domed tomb of a Karakhanid ruler, honoured in the heart of Taraz.',
    description:
      'The mausoleum of Karakhan stands in the centre of Taraz, one of the oldest cities of Kazakhstan. It was first built in the eleventh century over the grave of a ruler of the Karakhanid state, who is remembered in legend as a wise and just khan. People called him Aulie-Ata, "the holy father", and for many years the city itself carried this name. The building has a square base, a high portal and a dome, and was rebuilt on its old foundations at the beginning of the twentieth century. Legend links Karakhan with Aisha Bibi, the bride he lost, and the two monuments are often visited together.',
    facts: [
      'Karakhan was honoured as Aulie-Ata, "the holy father", and Taraz was once named after him.',
      'The Karakhanids ruled a large state in Central Asia in the tenth to thirteenth centuries.',
      'The mausoleum was rebuilt on its medieval foundations in the early twentieth century.',
    ],
    transcript:
      'Karakhan is a domed mausoleum in the centre of Taraz. It honours a medieval ruler remembered as Aulie-Ata, the holy father, who is linked in legend with Aisha Bibi.',
    model: {
      sketchfab: {
        uid: '2e9a13c3eb9e4f5f875cda5b5c110e59',
        url: sfUrl('2e9a13c3eb9e4f5f875cda5b5c110e59'),
        title: 'The Mausoleum of Karakhan',
        creator: 'Askhat Shulenbay',
        creatorUrl: `${SF}/shulenbay`,
        license: null,
        note: NO_LICENSE,
      },
      glb: glb('karakhan', 'Simplified 3D model of the Karakhan mausoleum'),
    },
  },
  {
    slug: 'airan',
    part: 1,
    title: 'Ayran',
    native: 'Айран',
    transcription: 'ayran',
    topic:
      'On a hot summer day, a guest in the yurt is offered a bowl of cold [[ayran]] mixed with water.',
    subtitle: 'The cool sour milk of summer',
    summary: 'A refreshing fermented milk drink served in every Kazakh home.',
    description:
      'Ayran is a traditional Kazakh drink made from fermented cow’s, sheep’s or goat’s milk. The milk is boiled, cooled until it is warm, and then a little old ayran, called the starter, is stirred in. After some hours it thickens and becomes pleasantly sour. Ayran is drunk on its own, mixed with cold water on hot days, or poured over food. It quenches thirst, keeps well and is good for digestion, so it was always at hand in the yurt. Ayran is also the beginning of other dairy foods: when it is strained and dried, it becomes qurt, the hard cheese balls that nomads carried on long journeys.',
    facts: [
      'A spoonful of the previous day’s ayran is used as a starter for the next batch.',
      'Ayran mixed with cold water is a favourite summer drink.',
      'Strained and dried ayran is used to make qurt.',
    ],
    transcript:
      'Ayran is a cool, sour drink made from fermented milk. A little old ayran is stirred into warm milk, and a few hours later a refreshing drink is ready.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=ayran`,
      glb: glb('airan', 'Simplified 3D model of a wooden bowl of ayran with a jug'),
    },
  },

  /* ============================================================== PART 2 */
  {
    slug: 'aitys',
    part: 2,
    title: 'Aitys',
    native: 'Айтыс',
    transcription: 'aytıs',
    topic:
      'At a holiday, two akyns face each other and answer each other’s verses with quick wit in an [[aitys]] while the crowd cheers.',
    subtitle: 'A duel of poets',
    summary: 'Two akyns improvise verses to the dombra and answer each other in rhyme.',
    description:
      'Aitys is a contest of improvised poetry. Two akyns, poet-singers, sit facing each other with their dombras and take turns singing verses that they make up on the spot. Each must answer the rival quickly, wittily and in rhyme, praising their own people, joking, arguing and asking sharp questions. The audience listens closely and decides who was wiser and quicker. Aitys was performed at feasts and gatherings, and great akyns such as Suyunbai Aronuly and Zhambyl Zhabayev became famous through it. Today aitys competitions are held on large stages and shown on television. Aitys is recognised by UNESCO as part of the intangible cultural heritage of humanity.',
    facts: [
      'The verses in aitys are improvised, not learned by heart.',
      'Aitys was inscribed on the UNESCO intangible heritage list in 2015.',
      'Akyns often accompany themselves on the dombra.',
    ],
    transcript:
      'Aitys is a duel of poets. Two akyns face each other with their dombras and improvise verses, answering each other quickly, wisely and in rhyme.',
    model: {
      sketchfab: {
        uid: 'ed85f3d93a684329a75ebfa1bb0d19c0',
        url: sfUrl('ed85f3d93a684329a75ebfa1bb0d19c0'),
        title: 'Bust of the Kazakh poet Suyunbai Aronuly',
        creator: 'Yerbol Kopeyev',
        creatorUrl: `${SF}/yerbol.kopeyev`,
        license: null,
        about: 'A bust of the famous aitys akyn Suyunbai Aronuly.',
        note: NO_LICENSE,
      },
      glb: glb('aitys', 'Simplified 3D model of two dombras facing each other on a carpet'),
    },
  },
  {
    slug: 'asyk',
    part: 2,
    title: 'Asyk',
    native: 'Асық',
    transcription: 'asıq',
    topic:
      'Children sit in a circle on the ground and throw the [[asyk]] bones, and every throw decides who wins the game.',
    subtitle: 'The knucklebone game',
    summary: 'Small sheep knucklebones used in the favourite game of Kazakh children.',
    description:
      'An asyk is the small knucklebone of a sheep. For centuries Kazakh children have used asyks to play many games. The best known is asyk atu, "shooting asyks": players set a row of asyks on the ground and try to knock them out with a heavier shooter called the saqa, often filled with lead. Each side of an asyk has its own name, and the way it lands matters in the game. Playing asyk trains a good eye, a steady hand and patience, and children kept their asyks in special bags and painted the best ones. Asyk games are recognised by UNESCO as part of the intangible cultural heritage of humanity.',
    facts: [
      'The heavy shooting piece is called the saqa.',
      'The four sides of an asyk have their own names, such as alshy and taiqy.',
      'Kazakh traditional asyk games were added to the UNESCO intangible heritage list in 2017.',
    ],
    transcript:
      'Asyk is the small knucklebone of a sheep and the favourite game of Kazakh children. Players shoot a heavy asyk to knock others out of a row.',
    model: {
      sketchfab: {
        uid: '2b1e7b47b43242c7b8027a3c4f6c400e',
        url: sfUrl('2b1e7b47b43242c7b8027a3c4f6c400e'),
        title: 'Asyk (Bone)',
        creator: 'AngryTengri',
        creatorUrl: `${SF}/angrytengri`,
        license: 'CC Attribution 4.0',
      },
      glb: glb('asyk', 'Simplified 3D model of a row of asyks and a shooter'),
    },
  },
  {
    slug: 'at-arba',
    part: 2,
    title: 'At Arba',
    native: 'Ат арба',
    transcription: 'at arba',
    topic:
      'Before cars and roads, a family loaded its belongings onto an [[at arba]], a cart pulled by a horse.',
    subtitle: 'The horse-drawn cart',
    summary: 'A wooden cart with tall wheels, pulled by a horse.',
    description:
      'An at arba is a cart drawn by a horse. It has a wooden body and two or four tall wooden wheels with strong spokes, which roll easily over rough steppe roads and through mud and shallow rivers. Two long shafts are fastened to the horse’s harness. Settled villages and families in winter quarters used the at arba to carry hay, firewood, water, grain and the harvest, and to take people to the market or to a celebration. Making a good cart, and especially its wheels, was the work of a skilled master. Today the at arba is still seen in villages and at festivals.',
    facts: [
      'Tall wheels help the cart cross rough ground, mud and streams.',
      'The cart is joined to the horse with two long shafts and a harness.',
      'Making strong wooden wheels required a skilled craftsman.',
    ],
    transcript:
      'At arba is a horse-drawn cart. Its tall wooden wheels roll over rough roads, carrying hay, water, firewood and people.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=horse%20cart`,
      glb: glb('at-arba', 'Simplified 3D model of a wooden horse cart with tall wheels'),
    },
  },
  {
    slug: 'baige',
    part: 2,
    title: 'Baige',
    native: 'Бәйге',
    transcription: 'bäyge',
    topic:
      'At a wedding or a holiday, men ride out on their horses for the [[baige]], and the fastest, best-trained horse brings honour to its owner.',
    subtitle: 'The long-distance horse race',
    summary: 'A thrilling horse race across the open steppe, held at every great celebration.',
    description:
      'Baige is the traditional Kazakh horse race, held at weddings, holidays such as Nauryz, and large celebrations. Unlike short races on a track, a baige can cover many kilometres across the open steppe, testing the endurance of the horses as much as their speed. The riders are often light, skilful boys, and the horses are prepared for weeks in advance. The whole crowd cheers as the riders appear on the horizon. Winning a baige brought honour to the horse’s owner and a valuable prize. The qamshy, a braided leather whip, is the rider’s constant companion and a symbol of the horseman.',
    facts: [
      'A baige can be many kilometres long and tests the endurance of horses.',
      'Riders are often young boys, because a light rider helps the horse.',
      'The qamshy, a braided whip, is a symbol of the Kazakh horseman.',
    ],
    transcript:
      'Baige is a long horse race across the open steppe. It is held at weddings and holidays, and the winner brings great honour to the horse’s owner.',
    model: {
      sketchfab: {
        uid: '82155f5df1d040149a529ea3b1a24cae',
        url: sfUrl('82155f5df1d040149a529ea3b1a24cae'),
        title: 'Qamshy (kamshy)',
        creator: 'Q3D_Library',
        creatorUrl: `${SF}/Q3D_Open_Library`,
        license: 'CC Attribution 4.0',
        about: 'The qamshy, the braided horse whip of the Kazakh rider.',
      },
      glb: glb('baige', 'Simplified 3D model of a race horse on a winner’s podium'),
    },
  },
  {
    slug: 'baursak',
    part: 2,
    title: 'Baursak',
    native: 'Бауырсақ',
    transcription: 'bauırsaq',
    topic:
      'The meal is accompanied by [[baursak]], small round pieces of fried dough, served hot with tea.',
    subtitle: 'Golden bread of the dastarkhan',
    summary: 'Small pieces of dough fried until golden and puffy.',
    description:
      'Baursak is fried dough, golden on the outside and soft inside. The dough is made from flour, milk or water, yeast and a little sugar, rolled out and cut into small squares, triangles or circles, then fried in hot oil until it puffs up. Baursak is served at almost every Kazakh table, the dastarkhan, with tea, butter, honey or jam, and it is piled high on plates at weddings and holidays. Many families keep a custom of frying baursak on Fridays and on memorial days, believing that the smell of fried bread reaches the spirits of the ancestors. A table without baursak hardly feels like a celebration.',
    facts: [
      'Baursak can be square, triangular or round.',
      'It is usually served with tea at the dastarkhan, the festive table.',
      'Frying baursak on Fridays is a custom in many families.',
    ],
    transcript:
      'Baursak is dough fried until it is golden and puffy. It is served with tea at every Kazakh table, from everyday meals to the biggest celebrations.',
    model: {
      sketchfab: {
        uid: '6a81e4875f454ec28163b514972713bc',
        url: sfUrl('6a81e4875f454ec28163b514972713bc'),
        title: 'Boortsog',
        creator: 'yelaman.arts',
        creatorUrl: `${SF}/elamanbolushan`,
        license: 'CC Attribution 4.0',
      },
      glb: glb('baursak', 'Simplified 3D model of a plate of baursak'),
    },
  },
  {
    slug: 'besik',
    part: 2,
    title: 'Besik',
    native: 'Бесік',
    transcription: 'besík',
    topic:
      'A newborn baby sleeps in a wooden [[besik]], and relatives gather for a small celebration when the baby is first laid in it.',
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
      'Besik is the wooden Kazakh cradle. Its rounded base rocks gently, soft ribbons hold the baby, and the besik toi celebrates the first time a child is laid in it.',
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
      glb: glb('besik', 'Simplified 3D model of a Kazakh besik cradle'),
    },
  },
  {
    slug: 'dombra',
    part: 2,
    title: 'Dombyra',
    native: 'Домбыра',
    transcription: 'dombıra',
    topic:
      'At the end of the meal you may sit and have tea while the musicians tune up the [[dombra]], a two-stringed instrument, and sing songs about love and war.',
    subtitle: 'The two-string voice of the steppe',
    summary: 'A long-necked, two-string instrument at the heart of Kazakh music.',
    description:
      'The dombyra is the best-loved instrument of the Kazakh people. Its small wooden body is attached to a long, slender neck, and two strings stretch along its length. Players strum or strike the strings with the right hand in quick, rhythmic patterns, while the left hand presses them against the frets to shape the melody. The dombyra accompanies the songs of the akyns, the traditional poet-singers, and carries the kui, short instrumental pieces that tell stories of nature, history and feeling. For generations it has been a companion at feasts, gatherings and quiet evenings, and a living voice of Kazakh memory.',
    facts: [
      'A kui is a short instrumental composition, often inspired by a legend, a landscape or an event.',
      'Akyns are poet-singers who improvise verse, often accompanied by the dombyra.',
      'In Kazakh families the dombyra is traditionally treated with great respect.',
    ],
    transcript:
      'Dombyra is the best-loved Kazakh instrument: a wooden body, a long neck and just two strings. It accompanies the songs of the akyns and plays the kui.',
    model: {
      sketchfab: {
        uid: 'c75f815bb74f426a9d923642c52f8f9a',
        url: `${SF}/3d-models/kazakh-dombra-c75f815bb74f426a9d923642c52f8f9a`,
        title: 'Kazakh Dombra',
        creator: 'Q3D_Library',
        creatorUrl: `${SF}/Q3D_Open_Library`,
        license: 'CC Attribution 4.0',
      },
      glb: glb('dombra', 'Simplified 3D model of a Kazakh dombyra'),
    },
  },
  {
    slug: 'zhailau',
    part: 2,
    title: 'Zhailau',
    native: 'Жайлау',
    transcription: 'zhaylau',
    topic:
      'In summer the herders move their yurts to the [[zhailau]], the cool mountain pasture, where the animals feed on fresh grass.',
    subtitle: 'The green summer pasture',
    summary: 'High summer meadows where families lived with their herds.',
    description:
      'The zhailau is the summer pasture. In late spring, nomadic families left their winter quarters and moved with their herds to cool mountain meadows or green river valleys, where the grass was rich and water was plentiful. There they raised their white yurts, and the animals grew strong over the summer. Life on the zhailau was the happiest time of the year: mares gave plenty of milk for kymyz, young people met at gatherings, and weddings, horse races and games were held. Songs and poems praise the beauty of the zhailau, with its flowers, springs and wide skies.',
    facts: [
      'Families moved to the zhailau in late spring and returned in autumn.',
      'Summer on the zhailau was the season of kymyz, weddings and festivals.',
      'Mountain meadows and river valleys made the best summer pastures.',
    ],
    transcript:
      'Zhailau is the summer pasture: green mountain meadows where nomadic families raised their yurts. It was the season of kymyz, songs, weddings and horse races.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=yurt`,
      glb: glb('zhailau', 'Simplified 3D model of a summer pasture with a yurt, sheep and a stream'),
    },
  },
  {
    slug: 'kazakh-kuresi',
    part: 2,
    title: 'Kazakh Kuresi',
    native: 'Қазақ күресі',
    transcription: 'qazaq küresí',
    topic:
      'At a holiday, wrestlers meet in [[Kazakh kuresi]] inside a ring of spectators and try to throw each other to the ground.',
    subtitle: 'The wrestling of the steppe',
    summary: 'Traditional belt wrestling, the sport of strong and honourable men.',
    description:
      'Kazakh kuresi is the national form of wrestling. Two wrestlers, called paluans, take hold of each other’s belts and try to throw the opponent onto his back using strength, balance and clever technique. In the past, wrestling matches were held at every great toi and festival, and the winner received a valuable prize such as a horse or a camel. A paluan was respected not only for his strength but also for his honour and fairness. The legendary Kazhymukan Munaitpasov, who became a world champion in the early twentieth century, is a hero of Kazakh wrestling. Today the tournament "Kazakhstan Barysy" crowns the strongest wrestler of the country.',
    facts: [
      'Kazakh wrestlers are called paluans.',
      'In traditional matches, wrestlers grip each other’s belts.',
      'Kazhymukan Munaitpasov is the most famous Kazakh wrestler of the past.',
    ],
    transcript:
      'Kazakh kuresi is national wrestling. Two paluans hold each other’s belts and try to throw the opponent onto his back with strength, balance and skill.',
    model: {
      sketchfab: {
        uid: 'd89a6ac3398a40d2af6ccaed23eb03f3',
        url: sfUrl('d89a6ac3398a40d2af6ccaed23eb03f3'),
        title: 'Kazhymukan Munaitpasov',
        creator: 'karaman.arman',
        creatorUrl: `${SF}/karaman.arman`,
        license: null,
        about: 'The legendary wrestler Kazhymukan Munaitpasov.',
        note: NO_LICENSE,
      },
      glb: glb('kazakh-kuresi', 'Simplified 3D model of a wrestling belt on a round mat'),
    },
  },
  {
    slug: 'keruen',
    part: 2,
    title: 'Keruen',
    native: 'Керуен',
    transcription: 'keruen',
    topic:
      'A long [[keruen]] of camels crossed the steppe, carrying goods between distant towns.',
    subtitle: 'The camel caravan of the Silk Road',
    summary: 'A long line of loaded camels crossing the steppe and the desert.',
    description:
      'A keruen is a caravan: a long line of camels, horses and people travelling together across the steppe and the desert. For centuries caravans followed the routes of the Great Silk Road through the land of present-day Kazakhstan, carrying silk, spices, cloth, metalwork and news between East and West. Two-humped Bactrian camels were ideal for this journey, because they can carry heavy loads and go a long time without water. Caravans stopped at wells and at caravanserais, roadside inns where travellers and animals rested. Cities such as Taraz, Otrar and Turkestan grew rich on the caravan trade.',
    facts: [
      'The Great Silk Road crossed the south of present-day Kazakhstan.',
      'Bactrian camels can carry heavy loads and go a long time without water.',
      'A caravanserai was a roadside inn for caravans.',
    ],
    transcript:
      'Keruen is a caravan: a long line of loaded camels crossing the steppe and the desert. Caravans on the Great Silk Road carried silk, spices and news.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=bactrian%20camel`,
      glb: glb('keruen', 'Simplified 3D model of a caravan of loaded camels'),
    },
  },
  {
    slug: 'kosh',
    part: 2,
    title: 'Kosh',
    native: 'Көш',
    transcription: 'kösh',
    topic:
      'When autumn came, the whole village joined the [[kosh]], loading the yurts and moving to the winter pastures.',
    subtitle: 'The great seasonal move',
    summary: 'The migration of a whole aul, with yurts packed on camels.',
    description:
      'Kosh is the move of a nomadic family or a whole aul, a village of yurts, from one pasture to the next. Several times a year, as the seasons changed, the yurts were taken down, and the felt, the lattice walls, the roof poles and the shanyraq were tied onto camels and horses together with chests, carpets and household goods. The kosh moved slowly across the steppe, with the herds walking alongside. A kosh was carefully organised and even beautiful: the leading camel was often decorated, and women and children rode in their best clothes. When the kosh arrived, the yurts were raised again within hours.',
    facts: [
      'An aul is a village of yurts that moved together.',
      'A dismantled yurt could be carried by one or two camels.',
      'The leading camel of a kosh was often decorated with carpets and tassels.',
    ],
    transcript:
      'Kosh is the seasonal move of nomads. The yurts were taken down and loaded onto camels, and the whole aul travelled with its herds to a new pasture.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=nomad%20camel`,
      glb: glb('kosh', 'Simplified 3D model of a camel carrying a folded yurt'),
    },
  },
  {
    slug: 'kymyz',
    part: 2,
    title: 'Kymyz',
    native: 'Қымыз',
    transcription: 'qımız',
    topic:
      'Guests in the yurt are offered a bowl of [[kymyz]], the sour mare’s milk drink, as a sign of hospitality.',
    subtitle: 'The fermented mare’s milk',
    summary: 'The famous drink of the steppe, served from a leather saba.',
    description:
      'Kymyz is fermented mare’s milk, the most treasured drink of the Kazakh steppe. Mares are milked several times a day in summer, and the fresh milk is poured into a saba, a large leather vessel, where it is stirred again and again with a wooden plunger called a pispek. Over time the milk ferments and becomes slightly fizzy, sour and refreshing. Kymyz is served in wooden bowls, the tostagan, with a ladle called an ozhau. It is offered to guests as a sign of honour and is valued as a healthy drink. In spring, the first kymyz of the year is celebrated with a feast called kymyzmuryndyk.',
    facts: [
      'Kymyz is made in a leather vessel called a saba.',
      'It is served in a wooden bowl, the tostagan, with a ladle, the ozhau.',
      'Kymyzmuryndyk is the spring feast of the first kymyz.',
    ],
    transcript:
      'Kymyz is fermented mare’s milk, the treasured drink of the steppe. It is stirred in a leather saba and served in wooden bowls to honoured guests.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=kumys`,
      glb: glb('kymyz', 'Simplified 3D model of a wooden bowl of kymyz with a ladle'),
    },
  },
  {
    slug: 'kui',
    part: 2,
    title: 'Kui',
    native: 'Күй',
    transcription: 'küy',
    topic:
      'Around the fire the musician plays a [[kui]] on the dombra, a melody that tells a story without any words.',
    subtitle: 'A story told without words',
    summary: 'An instrumental piece that tells a story through music alone.',
    description:
      'A kui is a piece of instrumental music, most often played on the dombyra, and also on the kobyz and the sybyzgy flute. A kui has no words, but it tells a story: the gallop of horses, a storm on the steppe, the sorrow of a lost loved one or a historic event. Before playing, a musician often tells the legend behind the kui, and then the instrument continues the story. Composers of kui are called kuishi. The greatest of them, Kurmangazy, wrote famous kuis such as "Sary-Arka" and "Adai", and Dina Nurpeisova and Tattimbet are also loved. Kui is the heart of Kazakh instrumental music.',
    facts: [
      'A kui is purely instrumental and has no sung words.',
      'Composers and performers of kui are called kuishi.',
      'Kurmangazy’s kui "Sary-Arka" is one of the best-known Kazakh melodies.',
    ],
    transcript:
      'A kui is an instrumental piece that tells a story without words. The galloping of horses, a storm or a legend come alive in the music of the dombyra.',
    model: {
      sketchfab: {
        uid: 'fd35fa3336034fcc870c18923d1dfcdc',
        url: `${SF}/3d-models/kazakh-national-instruments-fd35fa3336034fcc870c18923d1dfcdc`,
        title: 'Kazakh national instruments',
        creator: '3D витрина (ersa_kz)',
        creatorUrl: `${SF}/ersa_kz`,
        license: null,
        note: NO_LICENSE,
      },
      glb: glb('kui', 'Simplified 3D model of a dombyra with musical notes'),
    },
  },
  {
    slug: 'qorzhyn',
    part: 2,
    title: 'Qorzhyn',
    native: 'Қоржын',
    transcription: 'qorzhın',
    topic:
      'Before the journey, the rider hangs a pair of [[qorzhyn]] over the saddle, packed with bread and clothes.',
    subtitle: 'The double saddlebag',
    summary: 'A woven bag with two pockets, thrown over a horse or a camel.',
    description:
      'A qorzhyn is a double bag made of two pockets joined by a band. It is thrown over the back of a horse or a camel, with one pocket hanging on each side, so that the load stays balanced. Qorzhyns were woven or sewn from wool, felt and leather and decorated with bright geometric ornaments and tassels. Travellers carried food, clothes and gifts in them, and at home a qorzhyn hung on the wall of the yurt as a storage bag. A beautifully made qorzhyn showed the skill of the women who wove it and was often part of a bride’s dowry.',
    facts: [
      'The two pockets hang on each side of the saddle, keeping the load balanced.',
      'Qorzhyns are decorated with woven ornaments and tassels.',
      'In the yurt, a qorzhyn was hung on the wall for storage.',
    ],
    transcript:
      'Qorzhyn is a double saddlebag. Its two woven pockets hang on each side of a horse or camel, carrying food, clothes and gifts on the road.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=saddlebag`,
      glb: glb('qorzhyn', 'Simplified 3D model of a woven double saddlebag'),
    },
  },
  {
    slug: 'qudyq',
    part: 2,
    title: 'Qudyq',
    native: 'Құдық',
    transcription: 'quduq',
    topic:
      'After days of travel, the caravan stops at a [[qudyq]], a well, to give water to the animals.',
    subtitle: 'The well that gives life',
    summary: 'A well dug deep into the steppe to water people and herds.',
    description:
      'A qudyq is a well. On the dry steppe and in the desert, wells were a matter of life: without water, neither people nor herds could survive, and caravan and migration routes followed the line of the wells. Well-diggers were skilled and respected masters who knew where to find water underground. The walls were lined with stones or wood, and water was raised with a leather bucket called a qauga on a rope, sometimes pulled up by a camel or a horse. To dig a well for others was considered a great good deed, and many wells carry the name of the person who dug them.',
    facts: [
      'Migration and caravan routes followed the line of wells.',
      'Water was raised in a leather bucket called a qauga.',
      'Digging a well for others was considered a great good deed.',
    ],
    transcript:
      'Qudyq is a well. On the dry steppe, a well meant life for people and herds, and digging a well for others was a great good deed.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=old%20well`,
      glb: glb('qudyq', 'Simplified 3D model of a steppe well with a wooden frame and bucket'),
    },
  },
  {
    slug: 'qurt',
    part: 2,
    title: 'Qurt',
    native: 'Құрт',
    transcription: 'qurt',
    topic:
      'Before a long journey, the nomads put [[qurt]], dried salty cheese balls, into their bags.',
    subtitle: 'The dried cheese of the road',
    summary: 'Hard, salty balls of dried curd that keep for months.',
    description:
      'Qurt is a dried dairy food. Sour milk or ayran is boiled and strained through a cloth until a thick curd is left. The curd is salted, shaped by hand into small balls or rolls, and laid out in the sun and wind to dry until it is hard as stone. Qurt keeps for many months without spoiling, so nomads always had it on long journeys and through the winter. It is eaten as a snack, sucked slowly, or soaked and crushed into soups and drinks. Its taste is salty and sour. Today qurt is sold in every market of Kazakhstan, in white, smoked and flavoured varieties.',
    facts: [
      'Qurt is made from strained, salted curd that is dried in the sun.',
      'It keeps for months, which made it ideal food for travellers.',
      'Qurt can be eaten as it is or dissolved in water for soups and drinks.',
    ],
    transcript:
      'Qurt is dried curd shaped into small salty balls. It keeps for months, so nomads carried it on long journeys and through the winter.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=qurt`,
      glb: glb('qurt', 'Simplified 3D model of qurt balls on a wooden board'),
    },
  },
  {
    slug: 'qystau',
    part: 2,
    title: 'Qystau',
    native: 'Қыстау',
    transcription: 'qıstau',
    topic:
      'When the snow arrives, the family moves into the [[qystau]], a winter dwelling sheltered from the wind.',
    subtitle: 'The sheltered winter home',
    summary: 'Winter quarters in a protected valley, with houses and pens for the herds.',
    description:
      'The qystau is the winter quarters of a nomadic family. In late autumn, families returned from the summer pastures to a sheltered place, a valley, the foot of a hill or a riverbank with reeds, where the snow was shallower and the wind weaker. Here they often had permanent buildings of stone, clay or turf, along with pens and sheds that protected the animals from frost and wolves. Hay was cut in summer and stored for the winter. The qystau was used year after year and belonged to the same family for generations, so it was a place of deep attachment and memory.',
    facts: [
      'A qystau was chosen in a place protected from wind and deep snow.',
      'Winter buildings were made of stone, clay, turf or wood.',
      'The same family used its qystau year after year.',
    ],
    transcript:
      'Qystau is the winter home of nomads: a sheltered valley with houses and pens, where families and their herds waited out the cold months.',
    model: {
      sketchfab: {
        uid: '88d03e52d7f84257a6b7d68039492132',
        url: sfUrl('88d03e52d7f84257a6b7d68039492132'),
        title: 'Kazakh dwellings (XVIII-XIXc.)',
        creator: 'k.a.akishevinstitute',
        creatorUrl: `${SF}/k.a.akishevinstitute`,
        license: null,
        about: 'A model of Kazakh dwellings of the 18th–19th centuries.',
        note: NO_LICENSE,
      },
      glb: glb('qystau', 'Simplified 3D model of a winter house with a livestock pen'),
    },
  },
  {
    slug: 'saba',
    part: 2,
    title: 'Saba',
    native: 'Саба',
    transcription: 'saba',
    topic:
      'A leather [[saba]] hangs by the door of the yurt, and the housewife churns it to prepare kymyz.',
    subtitle: 'The leather vessel for kymyz',
    summary: 'A large leather vessel in which mare’s milk turns into kymyz.',
    description:
      'A saba is a large vessel made of smoked horse hide, used for making and storing kymyz. Its wide body narrows into a neck, and it stands on a wooden base or hangs inside the yurt, to the right of the entrance. Fresh mare’s milk is poured into the saba, and the family stirs it many times a day with the pispek, a long wooden plunger with a cross-piece at the end. Smoking the leather gives kymyz its special taste and keeps the vessel clean. A large saba could hold enough kymyz for many guests, and a full saba was a sign of wealth and hospitality.',
    facts: [
      'A saba is made of smoked horse hide.',
      'The milk inside is stirred with a wooden plunger called a pispek.',
      'A full saba was a sign of a generous and wealthy home.',
    ],
    transcript:
      'Saba is a large leather vessel for kymyz. Mare’s milk is poured inside and stirred with a wooden plunger, the pispek, until it ferments.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=leather%20vessel`,
      glb: glb('saba', 'Simplified 3D model of a leather saba with a wooden plunger'),
    },
  },
  {
    slug: 'shanyraq',
    part: 2,
    title: 'Shanyraq',
    native: 'Шаңырақ',
    transcription: 'shañıraq',
    topic:
      'Looking up inside the yurt, you see the daylight pour through the [[shanyraq]], the crown ring that stands for the family home.',
    subtitle: 'The crown of the yurt',
    summary: 'The wooden ring at the top of the yurt and a symbol of the family.',
    description:
      'The shanyraq is the wooden crown ring at the top of the yurt. The curved roof poles rest against it, and its crossed bars, the kuldiresh, form a dome in the middle. Through the opening of the shanyraq, light falls into the yurt and smoke from the hearth rises out, and at night the family could see the stars. The shanyraq is more than a part of the house: it is the symbol of the family and the home. It is passed down from generation to generation, traditionally kept by the youngest son in the parents’ home. Today the shanyraq appears on the coat of arms of Kazakhstan as a symbol of a shared home for all its people.',
    facts: [
      'The crossed bars inside the shanyraq are called kuldiresh.',
      'The family shanyraq is traditionally kept by the youngest son.',
      'The shanyraq is pictured at the centre of the coat of arms of Kazakhstan.',
    ],
    transcript:
      'Shanyraq is the wooden crown ring of the yurt. Light enters and smoke leaves through it, and it is the symbol of the family, passed down through generations.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=shanyrak`,
      glb: glb('shanyraq', 'Simplified 3D model of a shanyraq crown ring with crossed bars'),
    },
  },
  {
    slug: 'sheber',
    part: 2,
    title: 'Sheber',
    native: 'Шебер',
    transcription: 'sheber',
    topic:
      'A [[sheber]] spent weeks carving the wooden frame of a yurt, and his work was known across the steppe.',
    subtitle: 'The master craftsman',
    summary: 'A skilled maker of beautiful and useful things.',
    description:
      'A sheber is a master craftsman, a person with "golden hands". On the steppe, almost everything a family needed was made by hand: yurts and their wooden frames, cradles, chests, saddles, bowls, felt carpets, leather vessels and clothing. Shebers carved wood, pressed felt, tanned leather and embroidered patterns, and they decorated their work with traditional ornaments such as the ram’s horn, the qoshqar muiiz. Their skill was passed from master to apprentice and from parents to children. A sheber was greatly respected, because their work combined usefulness with beauty. Today Kazakh shebers keep these crafts alive in workshops and festivals.',
    facts: [
      'A sheber can work with wood, felt, leather, textiles or metal.',
      'The ram’s horn pattern, qoshqar muiiz, is one of the most common ornaments.',
      'Crafts were taught from master to apprentice.',
    ],
    transcript:
      'Sheber is a master craftsman with golden hands. Shebers carved wood, pressed felt and decorated their work with traditional ornaments.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=wood%20carving`,
      glb: glb('sheber', 'Simplified 3D model of a carved wooden chest with a chisel and mallet'),
    },
  },
  {
    slug: 'torsyk',
    part: 2,
    title: 'Torsyq',
    native: 'Торсық',
    transcription: 'torsıq',
    topic:
      'On the road, the horseman carries water in a leather [[torsyq]] tied to his saddle.',
    subtitle: 'The leather vessel of the road',
    summary: 'A sewn leather flask made for carrying drinks across the steppe.',
    description:
      'The torsyq is a traditional leather vessel for carrying and storing drinks, especially kymyz, the fermented mare’s milk beloved on the steppe. Craftsmen cut and sewed tanned hide into a rounded vessel with a narrow neck and handles, and often decorated it with embossed patterns. Light, durable and resistant to knocks, the torsyq suited a life on the move, when a rider needed to carry drink over long distances. The leather also helped keep the drink cool. Today the torsyq reminds us how ingeniously nomadic families made everyday objects from the materials of their herds.',
    facts: [
      'Kymyz is fermented mare’s milk, a traditional drink of the steppe.',
      'Leather decoration included embossing with carved wooden plates.',
      'Leather vessels came in several shapes for different kinds of drink.',
    ],
    transcript:
      'Torsyq is a leather flask for the road. Light and strong, it carried kymyz and water on long rides across the steppe.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=Kazakh%20torsyk`,
      glb: glb('torsyk', 'Simplified 3D model of a Kazakh torsyq leather flask'),
    },
  },
  {
    slug: 'usta',
    part: 2,
    title: 'Usta',
    native: 'Ұста',
    transcription: 'usta',
    topic:
      'The village [[usta]] heats the iron in the forge and hammers it into a horseshoe.',
    subtitle: 'The blacksmith master',
    summary: 'A master of metal who forged tools, horseshoes and weapons.',
    description:
      'An usta is a master, and above all a blacksmith. At the forge, the usta heated iron until it glowed, then shaped it on the anvil with a hammer. He made horseshoes, bits and stirrups for horses, knives, axes, scissors, cauldron hooks, door hinges and the metal parts of carts and chests, and in the past also weapons for warriors. Every aul needed an usta, because life with horses and herds depended on strong metal tools. The usta was respected as a wise and hard-working person, and the craft was often handed down from father to son.',
    facts: [
      'The usta worked at a forge with fire, bellows, hammer and anvil.',
      'He made horseshoes, stirrups, knives and many household tools.',
      'The craft was often passed down from father to son.',
    ],
    transcript:
      'Usta is a master blacksmith. He heated iron in the forge and shaped it on the anvil into horseshoes, knives and tools for the whole aul.',
    model: {
      sketchfab: {
        uid: '4b11b76fe069496ebd8ccd98f7d37ade',
        url: sfUrl('4b11b76fe069496ebd8ccd98f7d37ade'),
        title: 'Blacksmith’s Anvil',
        creator: 'm4rcu5j4ck50n',
        creatorUrl: `${SF}/m4rcu5j4ck50n`,
        license: 'CC Attribution 4.0',
        about: 'An anvil, the usta’s most important tool.',
      },
      glb: glb('usta', 'Simplified 3D model of an anvil with a hammer and horseshoe'),
    },
  },
  {
    slug: 'zerger',
    part: 2,
    title: 'Zerger',
    native: 'Зергер',
    transcription: 'zerger',
    topic:
      'A [[zerger]] works silver into earrings and bracelets for a bride.',
    subtitle: 'The silver jeweller',
    summary: 'A master who makes silver bracelets, rings and ornaments.',
    description:
      'A zerger is a jeweller, a master of silver and gold. Kazakh zergers made bracelets called bilezik, rings, earrings, hair pendants, buttons and decorations for belts, saddles and the bride’s saukele. They used fine techniques such as filigree, made of thin twisted wire, granulation with tiny metal balls, engraving and blackening with niello, and they set stones such as carnelian, coral and turquoise. Silver was believed to protect its wearer, so jewellery was more than an ornament. Each piece was given at important moments of life, such as a wedding or the birth of a child, and many are kept as family treasures.',
    facts: [
      'A bilezik is a bracelet; a zhuzik is a ring.',
      'Kazakh jewellers often set carnelian, coral and turquoise into silver.',
      'Silver jewellery was believed to protect the person who wore it.',
    ],
    transcript:
      'Zerger is a master jeweller. Zergers made silver bracelets, rings and earrings, decorated with fine wire patterns and stones such as carnelian and turquoise.',
    model: {
      sketchfab: null,
      searchUrl: `${SF}/search?type=models&q=silver%20bracelet`,
      glb: glb('zerger', 'Simplified 3D model of a silver bracelet and ring with stones'),
    },
  },
  {
    slug: 'zhyr',
    part: 2,
    title: 'Zhyr',
    native: 'Жыр',
    transcription: 'zhır',
    topic:
      'A [[zhyr]] is sung by a zhyrau, who tells the history and wisdom of the people to the sound of the kobyz.',
    subtitle: 'The epic song of heroes',
    summary: 'Long poems about heroes and history, sung by the zhyrau.',
    description:
      'Zhyr is epic poetry: long poems that tell of heroes, battles, journeys and the history of the people, sung or recited to the dombyra or the kobyz. The performers of zhyr, the zhyraus, were poets, storytellers and wise advisers. They knew thousands of lines by heart and could also compose their own verse. Famous zhyraus such as Asan Kaigy, Bukhar Zhyrau and Umbetai Zhyrau spoke to khans and to the people about justice, unity and the meaning of life. Heroic epics such as "Koblandy Batyr" and "Er Targyn" were passed down through zhyr for centuries, keeping the memory of the past alive.',
    facts: [
      'The singers of zhyr are called zhyraus.',
      'Zhyr is performed to the dombyra or the kobyz.',
      '"Koblandy Batyr" and "Er Targyn" are famous Kazakh heroic epics.',
    ],
    transcript:
      'Zhyr is epic song about heroes and history. The zhyrau, a poet and wise adviser, sang thousands of lines to the dombyra or the kobyz.',
    model: {
      sketchfab: {
        uid: '01248add15eb465eaf820a2bfbd8c9c2',
        url: sfUrl('01248add15eb465eaf820a2bfbd8c9c2'),
        title: 'Umbetai Zhyrau (Erementau)',
        creator: 'ahmedtawfeq',
        creatorUrl: `${SF}/ahmedtawfeq`,
        license: 'CC Attribution 4.0',
        about: 'A monument to the eighteenth-century poet Umbetai Zhyrau.',
      },
      glb: glb('zhyr', 'Simplified 3D model of a kobyz and an open book of verse'),
    },
  },
  {
    slug: 'kobyz',
    part: 2,
    title: 'Kobyz',
    native: 'Қобыз',
    transcription: 'qobız',
    topic:
      'The musician draws a bow across the [[kobyz]], and its deep, haunting sound recalls the legends of the steppe.',
    subtitle: 'The ancient bowed instrument',
    summary: 'A horsehair-stringed fiddle with a deep, haunting voice.',
    description:
      'The kobyz is an ancient bowed instrument of the Kazakh steppe. Its body is hollowed from wood and joined to a long neck, and it carries two strings made of horsehair. A bow, also strung with horsehair, is drawn across the strings while the player holds the instrument upright. Its low, husky, haunting voice was long associated with the baqsy, healers and shamans who played to ease suffering and guide spirits. Today the kobyz is remembered through the legend of Korkyt Ata, the sage and musician of Turkic tradition, and its music is performed on concert stages, keeping an ancient sound alive.',
    facts: [
      'The kobyz is a bowed instrument, unlike the plucked dombyra.',
      'Its strings and bow are traditionally made of horsehair.',
      'Korkyt Ata, a legendary sage, is closely associated with the kobyz in Turkic tradition.',
    ],
    transcript:
      'This is the kobyz, one of the oldest instruments of the Kazakh steppe. Unlike the dombyra, which is plucked, the kobyz is played with a bow. Both the bow and the two strings are traditionally made of horsehair, which gives the instrument its low, husky and slightly mysterious voice. The player holds the kobyz upright and draws the bow across the strings. In older times, the music of the kobyz was linked with the baqsy, healers who played to calm the sick and to speak with the spirits. The instrument is also tied to the legend of Korkyt Ata, a wise musician who, the stories say, played to push back death itself. Rotate the model and look at the hollowed body and the long neck. Listen with your imagination to a very old sound.',
    model: {
      sketchfab: {
        uid: 'c94229e78d834bd4bb465c287d7f01c1',
        url: `${SF}/3d-models/kazakh-qobyz-kobyz-c94229e78d834bd4bb465c287d7f01c1`,
        title: 'Kazakh Qobyz (Kobyz)',
        creator: 'Q3D_Library',
        creatorUrl: `${SF}/Q3D_Open_Library`,
        license: 'CC Attribution 4.0',
      },
      glb: glb('kobyz', 'Simplified 3D model of a Kazakh kobyz with its bow'),
    },
  },
  {
    slug: 'saukele',
    part: 2,
    title: 'Saukele',
    native: 'Сәукеле',
    transcription: 'säukele',
    topic:
      'The bride puts on a multi-layered white gown and a tall [[saukele]] with a long veil. When the veil falls behind her head, she has “opened her face” and the wedding ceremony is complete.',
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
        note: NO_LICENSE,
      },
      glb: glb('saukele', 'Simplified 3D model of a saukele bridal headdress'),
    },
  },
  {
    slug: 'shapan',
    part: 2,
    title: 'Shapan',
    native: 'Шапан',
    transcription: 'shapan',
    topic:
      'At the wedding, the groom wears the long [[shapan]] and a beautifully decorated hat.',
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
      sketchfab: {
        uid: '9dc71e54dbe14b87b4188a8a3826c95c',
        url: sfUrl('9dc71e54dbe14b87b4188a8a3826c95c'),
        title: 'Kazakh shapan',
        creator: 'karaman.arman',
        creatorUrl: `${SF}/karaman.arman`,
        license: 'CC Attribution 4.0',
      },
      glb: glb('shapan', 'Simplified 3D model of a Kazakh shapan robe'),
    },
  },
  {
    slug: 'beshbarmak',
    part: 2,
    title: 'Beshbarmak',
    native: 'Бесбармақ',
    transcription: 'besbarmaq',
    topic:
      'The guest sits at a low table and is served [[beshbarmak]], which means “five fingers”: noodles with onions and meat. An elder says a blessing and gives each part of the meal to a different person.',
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
      glb: glb('beshbarmak', 'Simplified 3D model of beshbarmak on a plate with a bowl of broth'),
    },
  },
];

export const objects = list.map((o, i) => ({ ...o, n: i + 1 }));
export const partOf = (o) => parts.find((p) => p.id === o.part);
export const chaptersOfPart = (id) => objects.filter((o) => o.part === id);

export const bySlug = (slug) => objects.find((o) => o.slug === slug) || null;
export const neighbours = (slug) => {
  const i = objects.findIndex((o) => o.slug === slug);
  return { prev: i > 0 ? objects[i - 1] : null, next: i >= 0 && i < objects.length - 1 ? objects[i + 1] : null };
};
export const videoSources = (o) => ({ mp4: `media/videos/${o.slug}.mp4`, webm: `media/videos/${o.slug}.webm` });
export const coverOf = (o) => `media/images/${o.slug}.jpg`;
export const audioUrlOf = (o) => `media/audio/${o.slug}.mp3`;
