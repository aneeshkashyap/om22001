const fs = require('fs');

const SHARES = [
  { id: '6af49506-0a44-83ec-85c1-6ecbbadda047', url: 'https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047' },
  { id: '6af49517-7c80-83ec-a422-4c8bde96cd14', url: 'https://chatgpt.com/share/6af49517-7c80-83ec-a422-4c8bde96cd14' },
  { id: '6af49529-ded8-83ee-ac96-a10049547724', url: 'https://chatgpt.com/share/6af49529-ded8-83ee-ac96-a10049547724' },
  { id: '6af49542-88b8-83ee-9b4a-769b1ec3d454', url: 'https://chatgpt.com/share/6af49542-88b8-83ee-9b4a-769b1ec3d454' },
  { id: '6af4955a-b0f0-83ec-bfa4-a3257b13a4de', url: 'https://chatgpt.com/share/6af4955a-b0f0-83ec-bfa4-a3257b13a4de' },
  { id: '6af49571-bafc-83e8-af94-15f7f6f48800', url: 'https://chatgpt.com/share/6af49571-bafc-83e8-af94-15f7f6f48800' },
  { id: '6af49588-ac1c-83ee-ab3e-b65021201e1d', url: 'https://chatgpt.com/share/6af49588-ac1c-83ee-ab3e-b65021201e1d' },
  { id: '6af4959d-3f40-83ee-a7bc-7562286c5b1b', url: 'https://chatgpt.com/share/6af4959d-3f40-83ee-a7bc-7562286c5b1b' },
];

async function checkAll() {
  for (let i = 0; i < SHARES.length; i++) {
    const s = SHARES[i];
    try {
      const res = await fetch(`https://chatgpt.com/backend-api/share/${s.id}`, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'application/json'
        }
      });
      const data = await res.json();
      console.log(`[Link ${i+1}] ID: ${s.id.slice(0, 10)}... | Title: "${data.title}" | Nodes count: ${Object.keys(data.mapping || {}).length}`);
      s.title = data.title;
      s.data = data;
      fs.writeFileSync(`scratch_chat_${i+1}.json`, JSON.stringify(data, null, 2));
    } catch (e) {
      console.error(`[Link ${i+1}] Error:`, e.message);
    }
  }
}

checkAll();

