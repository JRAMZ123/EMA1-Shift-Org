module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { password, content, message } = req.body || {};
    const expectedPassword = process.env.ADMIN_PASSWORD || '4dmin123';

    if (!password || password !== expectedPassword) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!content || typeof content !== 'string') {
      return res.status(400).json({ error: 'Missing HTML content to save' });
    }

    const token = process.env.GITHUB_TOKEN;
    const repo = process.env.GITHUB_REPO || 'JRAMZ123/EMA1-Shift-Org';
    const file = process.env.GITHUB_FILE || 'index.html';

    if (!token) {
      return res.status(500).json({ error: 'Missing GITHUB_TOKEN in environment variables' });
    }

    const url = `https://api.github.com/repos/${repo}/contents/${file}`;
    const headers = {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'ema1-org-chart'
    };

    const shaResponse = await fetch(url, { headers });
    const shaBody = await shaResponse.json();

    if (!shaResponse.ok) {
      return res.status(502).json({
        error: 'Failed to fetch the file from GitHub',
        details: shaBody
      });
    }

    const payload = {
      message: message || 'Org chart update',
      content: Buffer.from(content, 'utf8').toString('base64'),
      sha: shaBody.sha
    };

    const saveResponse = await fetch(url, {
      method: 'PUT',
      headers: {
        ...headers,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const saveBody = await saveResponse.json();

    if (!saveResponse.ok) {
      return res.status(500).json({
        error: 'GitHub update failed',
        details: saveBody
      });
    }

    return res.status(200).json({
      ok: true,
      message: 'Saved successfully',
      commit: saveBody.commit?.sha,
      html_url: saveBody.content?.html_url || `https://github.com/${repo}/blob/main/${file}`
    });
  } catch (error) {
    console.error('Save error:', error);
    return res.status(500).json({ error: 'Internal server error', details: error.message });
  }
};
