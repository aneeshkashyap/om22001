const URLS = [
  'https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047',
  'https://chatgpt.com/share/6af49517-7c80-83ec-a422-4c8bde96cd14',
  'https://chatgpt.com/share/6af49529-ded8-83ee-ac96-a10049547724',
  'https://chatgpt.com/share/6af49542-88b8-83ee-9b4a-769b1ec3d454',
  'https://chatgpt.com/share/6af4955a-b0f0-83ec-bfa4-a3257b13a4de',
  'https://chatgpt.com/share/6af49571-bafc-83e8-af94-15f7f6f48800',
  'https://chatgpt.com/share/6af49588-ac1c-83ee-ab3e-b65021201e1d',
  'https://chatgpt.com/share/6af4959d-3f40-83ee-a7bc-7562286c5b1b',
];

async function inspect(url, idx) {
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
      },
    });

    console.log(`[Link ${idx + 1}] Status: ${res.status}`);
    const html = await res.text();
    const titleMatch = html.match(/<title>([^<]+)<\/title>/);
    console.log(`[Link ${idx + 1}] Title: ${titleMatch ? titleMatch[1] : 'No title'}`);

    if (html.includes('__NEXT_DATA__')) {
      const parts = html.split('<script id="__NEXT_DATA__" type="application/json">');
      if (parts.length > 1) {
        const jsonPart = parts[1].split('</script>')[0];
        const data = JSON.parse(jsonPart);
        const serverResponse = data?.props?.pageProps?.serverResponse;
        console.log(`[Link ${idx + 1}] Shared conversation title:`, serverResponse?.data?.title);
        const linearMessages = serverResponse?.data?.linear_conversation || [];
        console.log(`[Link ${idx + 1}] Messages count:`, linearMessages.length);
        return {
          idx: idx + 1,
          url,
          title: serverResponse?.data?.title,
          messages: linearMessages,
        };
      }
    } else {
      console.log(`[Link ${idx + 1}] HTML snippet:`, html.slice(0, 300));
    }
  } catch (err) {
    console.error(`[Link ${idx + 1}] Failed:`, err.message);
  }
  return null;
}

async function run() {
  for (let i = 0; i < URLS.length; i++) {
    await inspect(URLS[i], i);
  }
}

run();

