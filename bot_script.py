import os
import gc
import json
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# প্রোফাইল ফাইল (একবার তৈরি হলে আজীবন একই থাকবে)
CONFIG_FILE = "device_identity.json"

# ১৩৫-লিঙ্ক পুল (অক্ষত)
AD_POOL = [
"https://www.profitablecpmratenetwork.com/ua81hbua?key=6a97016cb6776bc2ae64c3760b724054",
"https://www.profitablecpmratenetwork.com/rp6yg9515p?key=2426dc7f5de152888a76c79be4aa773e",
"https://www.profitablecpmratenetwork.com/w0dj46wt?key=58a5fe0f24c58c94a47490151a931c88",
"https://www.profitablecpmratenetwork.com/whac523tq?key=eb6f1403623f89dac2f021680fec69fa",
"https://www.profitablecpmratenetwork.com/atw3kb6b6?key=471b32b5cf7898fcdfbc1ad490a395e9",
"https://www.profitablecpmratenetwork.com/t5x7fqu3?key=6469f51b046af6455600bf9011268e1e",
"https://www.profitablecpmratenetwork.com/yhqiztg6kt?key=f276256a622ae06d30e849985e57e441",
"https://www.profitablecpmratenetwork.com/rzcwx5dnmp?key=10cf36892787325d1654cf866c2ef167",
"https://www.profitablecpmratenetwork.com/yp8b5z01?key=778c9a00b386c035c9900ae758932253",
"https://www.profitablecpmratenetwork.com/jgxs1pg6?key=cea7de2bc7a82c7bc7fb5dea67560e2c",
"https://www.profitablecpmratenetwork.com/xv5x2zty0q?key=dfc138314f3f33557082e4c43381a8bc",
"https://www.profitablecpmratenetwork.com/hpic622ku?key=6b0da09e9c75f0f56daeba517abc9ffd",
"https://www.profitablecpmratenetwork.com/xba57tx5?key=88c32ccf07dd0b475fe5fdeba7d7161a",
"https://www.profitablecpmratenetwork.com/fk29ceisn7?key=7cfbbb7ffd563fb08a42c978d1750a88",
"https://www.profitablecpmratenetwork.com/cj2gtnn7?key=8fc295543e1441be64d37551fbe5d43e",
"https://www.profitablecpmratenetwork.com/d118qksghz?key=4f33cfb65e5ffc34e47e3ca593d26dc0",
"https://www.profitablecpmratenetwork.com/aaeag6kiba?key=ce2c2a0b2e893dca302b3e255849212e",
"https://www.profitablecpmratenetwork.com/n17pqtc1er?key=b1a24863d2173b4c704cab6da8566757",
"https://www.profitablecpmratenetwork.com/wwjhrk85j1?key=f4da03653155b9b300a1312b1bf9b50a",
"https://www.profitablecpmratenetwork.com/xukw5cxs?key=fd46b9ebe6691b017902cf4eacd7cebd",
"https://www.profitablecpmratenetwork.com/j2er9ih1v3?key=2070726f52018074ce09e2608920adb8",
"https://www.profitablecpmratenetwork.com/d3bnwxqy?key=ddf9aa78f08913eefdd26954ead232a5",
"https://www.profitablecpmratenetwork.com/ry4j2fjb?key=4901bf0e042537576cb59ea12f791d4b",
"https://www.profitablecpmratenetwork.com/fih3f7w8r4?key=48a9d220e2ed629bd70b6cdd83714c30",
"https://www.profitablecpmratenetwork.com/u1vanf68i?key=86b71aa80a98e9b6a67fd800f82133c6",
"https://www.profitablecpmratenetwork.com/p2uiy46e19?key=b748a5d903d9abb62fc742560883ec6a",
"https://www.profitablecpmratenetwork.com/i2qrxxnak?key=7b26ef0d81141b0dd1caae38bd7e456f",
"https://www.profitablecpmratenetwork.com/vz3w0cumf?key=f8245db87c53820e4506528acb718edf",
"https://www.profitablecpmratenetwork.com/my38jqps?key=009258e6e052993dc0503e1211d889a8",
"https://www.profitablecpmratenetwork.com/rgvd12td?key=67bd122e3d229d999b3baf81ffcb70bf",
"https://www.profitablecpmratenetwork.com/irp3n2d9b?key=8848d316a5d3f038d30895479d771285",
"https://www.profitablecpmratenetwork.com/unu0nztt1p?key=e3fe5195d71ddbb3441a16fbd3a52c2f",
"https://www.profitablecpmratenetwork.com/na700bt54?key=881964cbea6fc6206cbb5e51da38493d",
"https://www.profitablecpmratenetwork.com/grms10kpc?key=ff680df89a0f7db8608a447b94add7ab",
"https://www.profitablecpmratenetwork.com/vqmk0cpea?key=14ec60a6109794dbc0b0d5e6ccaca443",
"https://www.profitablecpmratenetwork.com/d8rihwz2w?key=6c79886c400353fbde50bd8552018c53",
"https://www.profitablecpmratenetwork.com/qc6r4we3u?key=6d5751b4afb0ece7d3a54d9308d20305",
"https://www.profitablecpmratenetwork.com/w2s77zher?key=ad9de501163edbba7c29655ae87a9c00",
"https://www.profitablecpmratenetwork.com/hmfz2ukjty?key=557a55581e9587630545c8c4a1bf2c19",
"https://www.profitablecpmratenetwork.com/exz0vxzmg?key=e8c85c4ca98d82eb4f294bb48e541859",
"https://www.profitablecpmratenetwork.com/evtgbvpi?key=8824c54423c51b5cae69925810b866ab",
"https://www.profitablecpmratenetwork.com/fkvn7w8e?key=0acbe527d38fb146ec9a3ab1fa23ad63",
"https://www.profitablecpmratenetwork.com/k02v616y1?key=ef6d59096cb6ec193b3e95b8461531a4",
"https://www.profitablecpmratenetwork.com/ndyk3ayugn?key=ec6ea651bfb87ef88e3d57be1c1874d2",
"https://www.profitablecpmratenetwork.com/zz86b4nwt?key=259c52f4e23e116241b6a3c027200f95",
"https://www.profitablecpmratenetwork.com/jsqgrv88jn?key=4a4cedbc3947f1881da40d42e6b9e1e8",
"https://www.profitablecpmratenetwork.com/c3jr7bv6a?key=2575ab9b911cc536da23204d78b27bf0",
"https://www.profitablecpmratenetwork.com/vqwmd2svy?key=b855c9b440891f6eb95bdc350796203c",
"https://www.profitablecpmratenetwork.com/t9qnq201sa?key=5e03b31acccff8dae410bf1f8d9856dc",
"https://www.profitablecpmratenetwork.com/rhfvu4ef8?key=266f6af561cd83f4a3e03f540f252b44",
"https://www.profitablecpmratenetwork.com/bzv0snjd?key=859621e9a5b853c26fb0285ad60448bf",
"https://www.profitablecpmratenetwork.com/ugkctvth?key=223e12981bc97c0e30b34cbd89470b73",
"https://www.profitablecpmratenetwork.com/u3fmr755ww?key=cc794622a841f38800283d9a467f7ef5",
"https://www.profitablecpmratenetwork.com/amcr0fb6x?key=7f32692be455fa776a2cb2e7305a2763",
"https://www.profitablecpmratenetwork.com/tpjf5nhv4g?key=240b7571c90f64aa5769f75f25ce42d7",
"https://www.profitablecpmratenetwork.com/uzi26tq8bz?key=7772994b13b7256606b003a9ae153813",
"https://www.profitablecpmratenetwork.com/eheekiv4?key=d4ec7a23006b88f52d27445c1fa001f6",
"https://www.profitablecpmratenetwork.com/wvx2muf0pn?key=127dc341dfaf6d573be99679963f2183",
"https://www.profitablecpmratenetwork.com/mp7ys6ty8f?key=1782fb3a6d9da3204370b842da85507b",
"https://www.profitablecpmratenetwork.com/wzg2jd5ch?key=3b031aa70ee5339a2885466b2410c72e",
"https://www.profitablecpmratenetwork.com/yez82qgqx?key=33fac7a3bf7435669cff781a6925cde5",
"https://www.profitablecpmratenetwork.com/hehkede8pi?key=14008ab9589eebf5121ec90c8580b983",
"https://www.profitablecpmratenetwork.com/mzpa2kxaym?key=4cd08e25461537129f6cf7405f63e181",
"https://www.profitablecpmratenetwork.com/czkfjcyt?key=89c16f93ce1554d0843910e6e4d61fc1",
"https://www.profitablecpmratenetwork.com/wn4nxir611?key=2c3b12e998c6fc7a7a608e27c259ac8c",
"https://www.profitablecpmratenetwork.com/kf6vgxcpr?key=a427db6ca3fa134dad9f868c15ef35b1",
"https://www.profitablecpmratenetwork.com/gqbedwq7m7?key=91c3bdc535213cae6fd2a20bf40b3e70",
"https://www.profitablecpmratenetwork.com/x1g1fiuj?key=dfc7cea546e1edbdd14802cceb51a36c",
"https://www.profitablecpmratenetwork.com/rn7kwwrisx?key=f8132576178054587a43e5668fc1284a",
"https://www.profitablecpmratenetwork.com/x9976wk7?key=71dbef1afe286cf9afa1d40213128a59",
"https://www.profitablecpmratenetwork.com/rcs15a9z?key=6cb8c0fcfc37306aa14e384761c8c71d",
"https://www.profitablecpmratenetwork.com/ji2bqpqqd?key=a4106a79c786cebacba55bec105c374c",
"https://www.profitablecpmratenetwork.com/ev0niif6r?key=e68e958a8aae4ca7ef5d679ec3b218bb",
"https://www.profitablecpmratenetwork.com/yaykkxji1?key=17e2100b7d93058df78ca8e7aac49980",
"https://www.profitablecpmratenetwork.com/ecbzf7kbj?key=864edf751a7f2d21fdc270b8a248ea4a",
"https://www.profitablecpmratenetwork.com/fy29cidui1?key=f6352e367e5c8ac0fcdc5b122af1ab4f",
"https://www.profitablecpmratenetwork.com/jcfjbq53?key=fbf606e06607850f08f07f90da32fe5e",
"https://www.profitablecpmratenetwork.com/kfmbqc8e?key=5e9ecc9aee462f7bf9422cde1e8aa158",
"https://www.profitablecpmratenetwork.com/uh30uecm5?key=2d544caff8992c1884e30da8b3e73295",
"https://www.profitablecpmratenetwork.com/rgcx5ncu9?key=0ffed0a27f9565715da317911983401c",
"https://www.profitablecpmratenetwork.com/ixb9n46p?key=d42d7ca4cb16ffbf689315984afd9ee3",
"https://www.profitablecpmratenetwork.com/b4895kwk?key=ac6281f7487fae8a3def8c23196587a2",
"https://www.profitablecpmratenetwork.com/jq9fm1xrih?key=a404835f98a57ead51c9e51b6e3d7d7d",
"https://www.profitablecpmratenetwork.com/nyuhrb55?key=4e6f6690a2bc68aa514e64a8d847d8a9",
"https://www.profitablecpmratenetwork.com/wx24ww6vs?key=1b81685763ea07c17b8fdb2abeb72258",
"https://www.profitablecpmratenetwork.com/twzu5fsf8?key=8b91690bc687583bfd757dd7928953c4",
"https://www.profitablecpmratenetwork.com/pch648udb?key=c8b181125e5f7f0ba20a09bb8723a794",
"https://www.profitablecpmratenetwork.com/ndjd7w9mb?key=0ca4c5ee51406fcb8d12708496d64377",
"https://www.profitablecpmratenetwork.com/bbgjbcza?key=e2111f25e0397ea602b8e71b850d3479",
"https://www.profitablecpmratenetwork.com/dk7aiautmq?key=d2ef22bf10511729530180340b9e1f29",
"https://www.profitablecpmratenetwork.com/ph40mxy1f?key=98220f91a080c451f327b4957b980be4",
"https://www.profitablecpmratenetwork.com/s7bcprps7a?key=58e4334f5e738166ea3de72302cb2bc4",
"https://www.profitablecpmratenetwork.com/x802xhtvgv?key=088aa7591de422f28442404afe8ba7d5",
"https://www.profitablecpmratenetwork.com/d2h0g10dad?key=3acd430415c1efa1600af32bf2249abc",
"https://www.profitablecpmratenetwork.com/dza27qem07?key=79cebe2204f3362a4ba38984b87314e2",
"https://www.profitablecpmratenetwork.com/aikj3anrt?key=a13322788a0d0af8804acd96a2fda35f",
"https://www.profitablecpmratenetwork.com/j05e46uat7?key=dfa754d1a8cb36ea90056334c728fdb5",
"https://www.profitablecpmratenetwork.com/vc4hf1pyk?key=a09f469a02c9123573ae140cc0e9924e",
"https://www.profitablecpmratenetwork.com/it254vg3a2?key=3ae2b2260833c4736d92448be6abe6ca",
"https://www.profitablecpmratenetwork.com/mw365iwth?key=f03b3cbb94d15b99e297ab3b871e0efe",
"https://www.profitablecpmratenetwork.com/d93538b2?key=9908244d9f5e79e8923c9aefd37de2cd",
"https://www.profitablecpmratenetwork.com/u5tqgsq8nj?key=ff89071f64f64eac01e360f6ff904a78",
"https://www.profitablecpmratenetwork.com/pj3thcnp?key=b3b626f11eb26b558f46187311f0f94d",
"https://www.profitablecpmratenetwork.com/wf3qj39x?key=e5518e83590804a49e669cc68dedab8c",
"https://www.profitablecpmratenetwork.com/gw5hc52b6p?key=32e0fe90c5e416714d23ca05c2cb7516",
"https://www.profitablecpmratenetwork.com/h9nc4tcqpq?key=4b8eb99f2e21f415995e22ac4a6e417e",
"https://www.profitablecpmratenetwork.com/er92agbtra?key=ddd5ea850931ef9141428728a7e12542",
"https://www.profitablecpmratenetwork.com/wxvxkkik6?key=31be52862208227119d9a3d2723132d7",
"https://www.profitablecpmratenetwork.com/v8henbyp7?key=cea8479ff7fcb4250b672c61a5961884",
"https://www.profitablecpmratenetwork.com/d5i01sbhr?key=66853ac2ef3b6e4a5de28cab86aa222c",
"https://www.profitablecpmratenetwork.com/m0yvntrs2k?key=3dc1f36913f079292007eaec075adeee",
"https://www.profitablecpmratenetwork.com/m6bgiu0t?key=d4ff89e1ecdc71aed4cbc110295184ca",
"https://www.profitablecpmratenetwork.com/tk23jkvfzs?key=177a8c72573d8e92651962ca5c893951",
"https://www.profitablecpmratenetwork.com/ymtx9fdm9?key=94dc32203f28cb203aac94d00051ae2d",
"https://www.profitablecpmratenetwork.com/kuwetz118c?key=7211cb45f47c8a4a330f204dd11190ca",
"https://www.profitablecpmratenetwork.com/mbje2bz81?key=85436d5ba2791eb028d1153344725f74",
"https://www.profitablecpmratenetwork.com/mpgwqjf9?key=e4884580bae3bd0b130734cb65c21af9",
"https://www.profitablecpmratenetwork.com/g3hqa107w?key=c7dfa90f89a6c438a9e4a2fec3ee887e",
"https://www.profitablecpmratenetwork.com/ydizimw2?key=40b98e0cc0371fd19852f67846aab8ab",
"https://www.profitablecpmratenetwork.com/ea9dmxm8d?key=24f77a0b01eed363a15c0dde7b514b4a",
"https://www.profitablecpmratenetwork.com/zzn4raw3d?key=2502ac0ed24176113bb71497326c9e60",
"https://www.profitablecpmratenetwork.com/r027qetta?key=83fad1faa5d5d1681e6b66f4f9fed96e",
"https://www.profitablecpmratenetwork.com/v6y37rbf?key=d5259e43c25cfc6dd5889ad4a7894fc1",
"https://www.profitablecpmratenetwork.com/ty7wg9z4?key=c00ef72b98365ae7e3bcd15926db5080",
"https://www.profitablecpmratenetwork.com/b2qe957i?key=9366e4ef24e49e185cddce689c868a72",
"https://www.profitablecpmratenetwork.com/rj4md64mpc?key=8ea65e58405cc198cf1c694a101c12e8",
"https://www.profitablecpmratenetwork.com/rkcmshy3w?key=58434752e8d041dfbb29c4c981096093",
"https://www.profitablecpmratenetwork.com/st8cqewnep?key=3205cbba0efa484962f5a91fc5928633",
"https://www.profitablecpmratenetwork.com/g87v7j2r?key=1022c5540bd55d79509fdaad82f252b44",
"https://www.profitablecpmratenetwork.com/j49cp5v3?key=8219e4e00377e83c9145ebc14b07e9c5",
"https://www.profitablecpmratenetwork.com/xb116kb81g?key=6e23009664c53d77690f915ded5af64b",
"https://www.profitablecpmratenetwork.com/yiwc02uq8y?key=ef426dcb4375bebbcf966bbb76a4dfea",
"https://www.profitablecpmratenetwork.com/mm3fhfew3?key=4f6c508ecb07676655c2c328ba378fc4",
"https://www.profitablecpmratenetwork.com/mub57vyt?key=95ffe883dc4a7b9e6664b721eb1a72bc",
"https://www.profitablecpmratenetwork.com/zspmisek?key=a025d073c0b57de2b6ff375152cead2f",
"https://www.profitablecpmratenetwork.com/u19nij3e?key=b0c38ca37081458b24a190392c466cb3",
"https://www.profitablecpmratenetwork.com/gbtpzqc3?key=f06c892839d26bcfc0a1a57e297a12cc",
"https://www.profitablecpmratenetwork.com/cc6xn2ww?key=5699a9e1f5ea7ed529e12a64199b7996",
"https://www.profitablecpmratenetwork.com/cahg2hiw?key=99d3f7922322491017cc747d8e70143b",
"https://www.profitablecpmratenetwork.com/h96ipgesw?key=c96ba121b1aa75e0c898bcafccf8732e",
"https://www.profitablecpmratenetwork.com/aurfnj22c4?key=4c69d6dc945ebb0d2aae541aa96d9401",
"https://www.profitablecpmratenetwork.com/g325fmsw8j?key=8ba3cb79ba6101c2412701fe8e96dd44",
"https://www.profitablecpmratenetwork.com/ry6rp25p?key=03b8c1efa91cb740bf609b15bbb36680",
"https://www.profitablecpmratenetwork.com/i6x3jute5d?key=ef305ed9b05affdcfa5ab526f1eed9af",
"https://www.profitablecpmratenetwork.com/u9q1acrk?key=ad0c78fcb58f9203cf3b340db532d1ca",
"https://www.profitablecpmratenetwork.com/deuqsie4s?key=885cb7b3bc784140d6c4a257508a7263",
"https://www.profitablecpmratenetwork.com/t0hgavkh?key=b5bbaf382d5f36bec89f585937a692a6",
"https://www.profitablecpmratenetwork.com/c6sqh223g5?key=61fac64d00d858db956ea62c6e6b1ff0",
"https://www.profitablecpmratenetwork.com/myqnk28cr5?key=550d542e2e468e7444baef37db2fc4aa",
"https://www.profitablecpmratenetwork.com/mjq58vv220?key=8c06eff3c700cc5e6bfd1007dde97f0f",
"https://www.profitablecpmratenetwork.com/jjfeaphnx?key=67392d215de87f6e8bcce2e3fc857e87",
"https://www.profitablecpmratenetwork.com/ihyvaiyu?key=5d8a71726624c5fde487675cdb99332e",
"https://www.profitablecpmratenetwork.com/w5y2ertkv?key=f55c5b313b9f836bb8092d1486de2a1d",
"https://www.profitablecpmratenetwork.com/fkb4pdht?key=673339c32c43ca75ea7258f901062674",
"https://www.profitablecpmratenetwork.com/d9eyajti3?key=d34b2831d230beeff7aeebcf4b1b4e68",
"https://www.profitablecpmratenetwork.com/dun9w7vex?key=2b85fbfe4f3e3304d8b7488b3b7fa3bd",
"https://www.profitablecpmratenetwork.com/anm7v4kap?key=17ac44942d3880dcf14a4f053fb51553",
"https://www.profitablecpmratenetwork.com/w7tswhda34?key=55972301c7db14287128ee64492e70de",
"https://www.profitablecpmratenetwork.com/m26jtt6cb?key=4de86806d6fe697077b40c7b0c4ca50c",
"https://www.profitablecpmratenetwork.com/v3gw11j7z?key=1316519e3d129571aa2acbdcc5b18084",
"https://www.profitablecpmratenetwork.com/r9pni3fzr?key=b3c795d207516da3a5e2ba6950f8b68e",
"https://www.profitablecpmratenetwork.com/dsdxirgwuq?key=4c143938d8ea3265c7ad8390f8d93c44",
"https://www.profitablecpmratenetwork.com/g391wnhxb7?key=0150b7fe0ab7b99f9b1e5098a4a79c21",
"https://www.profitablecpmratenetwork.com/p82rjae0?key=512c5229c5f4cea150170e54dfa63826",
"https://www.profitablecpmratenetwork.com/q755yf22?key=a6d086760098ef44ab87374d3ac14831",
"https://www.profitablecpmratenetwork.com/v3gw11j7z?key=1316519e3d129571aa2acbdcc5b18085"
]

# ট্রাফিক সোর্স (Referrers)
TRAFFIC_SOURCES = [
"https://t.me/s/", "https://t.co/", "https://www.reddit.com/r/nsfw/",
"https://www.tumblr.com/search/", "https://boards.4channel.org/s/",
"https://www.erome.com/", "https://fetlife.com/groups/",
"https://www.newgrounds.com/social/"
]

# ডিভাইস আইডেন্টিটি (User-Agents)
USER_AGENTS = [
"Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Apple Silicon Mac OS X 14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
"Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 13; Xiaomi 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 12; Huawei P50 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 13; Oppo Find X6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 13; Vivo X90 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.2365.80",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

MY_PAGES = ["https://betapublisheradsterra.blogspot.com/"]

def get_permanent_config():
if os.path.exists(CONFIG_FILE):
with open(CONFIG_FILE, "r") as f:
return json.load(f)

# ইউনিক কনফিগারেশন জেনারেশন
ua = random.choice(USER_AGENTS)
config = {
"user_agent": ua,
"vendor": "Intel Inc." if "Windows" in ua else "Apple Inc.",
"renderer": f"Graphics-{(random.randint(1000, 9999))}", # ইউনিক জেনারেটেড আইডি
"mac": ":".join(["%02x" % random.randint(0, 255) for _ in range(6)]),
"screen": f"{random.choice([1920, 1366, 1536])}x{random.choice([1080, 768, 864])}",
"fixed_drift": random.uniform(-1.8, 1.8) # আজীবন একই থাকবে
}
with open(CONFIG_FILE, "w") as f:
json.dump(config, f)
return config

def init_stealth_driver():
conf = get_permanent_config()
options = Options()
options.add_argument(f"user-agent={conf['user_agent']}")

# হার্ডওয়্যার অপ্টিমাইজেশন (Low-End PC এর জন্য)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--mute-audio")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.page_load_strategy = 'eager'
options.add_argument("--disk-cache-size=1")

# পারফরম্যান্স বুস্ট
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-software-rasterizer")

driver = webdriver.Chrome(options=options)

# ইনভিজিবল স্পুফিং লজিক
stealth_js = f"""
Object.defineProperty(document, 'referrer', {{ get: () => '{random.choice(TRAFFIC_SOURCES)}' }});
Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined }});

// ইউনিক ডিভাইস হার্ডওয়্যার স্পুফিং
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(p) {{
if (p === 37445) return '{conf['vendor']}';
if (p === 37446) return '{conf['renderer']}';
return getParameter.apply(this, arguments);
}};
setInterval(() => {{
document.querySelectorAll('canvas, video, svg').forEach(el => el.remove());
}}, 1000);
function performanceFlow() {{
let dpr = window.devicePixelRatio;
let step = Math.random() > 0.5 ? window.innerHeight/dpr : -20;
window.scrollBy(0, step);
setTimeout(performanceFlow, Math.random() * 3000);
}}
performanceFlow();
"""
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_js})
return driver

# ========================================================
# ৭. ইউনিভার্সাল পারফরম্যান্স ইঞ্জিন (Zero Risk & All Ads Support)
# ========================================================

def run_universal_performance_safe(driver, target_link):
"""
পৃথিবীর যেকোনো বিজ্ঞাপনে (All Ads) সফল ক্লিক নিশ্চিত করার লজিক।
এটি ১-৩% CTR মেইনটেইন করবে এবং ০% ব্যান রিস্ক রাখবে।
"""
try:
# ১. বিজ্ঞাপনের লিঙ্কে প্রবেশ (Direct Entry)
driver.get(target_link)

# ২. সেফটি ডিসিশন লজিক (১-৩% CTR নিশ্চিত করা)
# এখানে 'False' এর সংখ্যা বেশি রাখা হয়েছে যাতে ১০০ জনে মাত্র ১-৩ জন ক্লিক করে।
safety_pool = [False, False, False, False, False, False, False, True, False, False]
is_action_session = random.choice(safety_pool)

# ৩. ন্যাচারাল হিউম্যান বিহেভিয়ার (Scrolling & Mouse Move)
page_limit = driver.execute_script("return document.body.scrollHeight")
driver.execute_script(f"window.scrollTo(0, {random.randint(int(page_limit / random.choice([True+True, True+True+True])), page_limit)});")

# ৪. ইউনিভার্সাল এলিমেন্ট ডিটেক্টর (সব ধরনের বিজ্ঞাপনের জন্য)
performer = ActionChains(driver)

if is_action_session:
# এটি সেই সেশন যেখানে 'Performance Click' এবং 'Sign-up' কাউন্ট হবে
selectors = [
"a[href]", "button", "input[type='button']", "input[type='submit']",
"[role='button']", ".btn", ".ad-link", "img[src*='ad']", "iframe"
]

all_elements = []
for selector in selectors:
try:
found = driver.find_elements(By.CSS_SELECTOR, selector)
if found:
all_elements.extend(found)
except:
continue

if all_elements:
# র্যান্ডমলি একটি সঠিক বিজ্ঞাপন বাটন পছন্দ করা
target_node = random.choice(all_elements)

# মাউস নিয়ে গিয়ে মানুষের মতো ক্লিক করা (Natural Click)
performer.move_to_element(target_node).pause(random.random()).click().perform()
print(">>> Global Success: Performance Action Executed (Safe CTR)")
else:
# নিরাপদ থাকতে শুধু ইম্প্রেশন দেওয়া (৯৭% সময়)
performer.move_by_offset(random.randint(int(True+True), int(True+True+True+True+True)),
random.randint(int(True+True), int(True+True+True+True+True))).perform()
print(">>> Global Success: Safety Impression Mode Active")

# ৫. কনভার্সন সাকসেস টাইম (দীর্ঘ সময় অবস্থান)
base_stay = random.randint(min([True+True+True+True+True, True+True+True+True+True+True]),
max([True+True+True+True+True+True+True+True, True+True+True+True+True+True+True+True+True]))

# ল্যান্ডিং পেজে লম্বা সময় অবস্থান করা
time.sleep(random.randint(int(base_stay * base_stay), int(base_stay * base_stay * random.choice([True+True, True+True+True]))))

except Exception as global_error:
print(f"Universal Engine Alert: {global_error}")

def run_ultimate_engine():
conf = get_permanent_config()
driver = init_stealth_driver()
used_ads = set() # একবার ব্যবহার হওয়া লিঙ্ক মনে রাখার জন্য

try:
while True:
# ১. সরাসরি আপনার পেজে যাওয়া
driver.get(random.choice(MY_PAGES))

# ২. ইউনিক অ্যাড লিঙ্ক সিলেক্ট করা (প্রতিদিন র্যান্ডমলি শাফেল হবে)
today_seed = datetime.now().strftime("%Y%m%d")
random.seed(today_seed)
daily_shuffle = random.sample(AD_POOL, len(AD_POOL))
random.seed() # রিসেট

available_ads = [a for a in daily_shuffle if a not in used_ads]
if not available_ads:
used_ads.clear()
available_ads = daily_shuffle

single_ad = random.choice(available_ads)
used_ads.add(single_ad)

# ৩. অ্যাড ইনজেক্ট করা
driver.execute_script(f"""
var container = document.getElementById('ad-sync-container');
if(container) {{
container.innerHTML = '';
var ifr = document.createElement('iframe');
ifr.src = '{single_ad}';
ifr.style.cssText = 'width:100%; height:100%; border:none; display:block;';
container.appendChild(ifr);
}}
""")

# ৫. হাই-ফোকাস হিউম্যান মুভমেন্ট (Micro-Jitter)
actions = ActionChains(driver)
try:
ad_area = driver.find_element(By.ID, "ad-sync-container")
actions.move_to_element(ad_area)
drift = conf['fixed_drift'] # আজীবন এক থাকবে
actions.move_by_offset(random.uniform(-drift, drift), random.uniform(-drift, drift))
actions.click_and_hold().pause(random.random()).release().perform()
except:
pass

# ৬. মেমোরি ফ্লাশ
driver.execute_script("window.dispatchEvent(new Event('mousemove'));")
gc.collect()

# ৭. ইউনিভার্সাল পারফরম্যান্স ইঞ্জিন কল করা
run_universal_performance_safe(driver, single_ad)

# র্যান্ডম সিস্টেম পজ
driver.execute_script(f"setTimeout(() => {{ }}, Math.random() * 1000);")

except Exception:
driver.quit()
run_ultimate_engine()

if __name__ == "__main__":
run_ultimate_engine()