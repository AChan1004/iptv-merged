import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin

SOURCES = [
    'https://raw.githubusercontent.com/sammy0101/hk-iptv-auto/refs/heads/main/hk_live.m3u',
    'https://iptv-org.github.io/iptv/countries/hk.m3u',
    'https://epg.pw/test_channels_hong_kong.m3u',
    'https://iptv-org.github.io/iptv/index.m3u',
]

def read_source(url):
    req = Request(url, headers={'User-Agent': 'IPTV-Playlist-Merger/1.0'})
    with urlopen(req, timeout=120) as response:
        base = response.url
        raw = response.read(50000001)
    if len(raw) > 50000000:
        raise ValueError('Source too large: ' + url)
    lines = [s.strip() for s in raw.decode('utf-8-sig').splitlines() if s.strip()]
    if not lines or not lines[0].startswith('#EXTM3U'):
        raise ValueError('Not an extended M3U: ' + url)
    if any(s.startswith('#EXT-X-') for s in lines):
        raise ValueError('HLS manifest is not a channel list: ' + url)
    entries, pending = [], []
    for line in lines[1:]:
        if line.startswith('#EXTINF:'):
            pending = [line]
        elif line.startswith('#'):
            if pending:
                pending.append(line)
        elif pending:
            stream = urljoin(base, line)
            if stream.startswith(('http://', 'https://', 'rtsp://', 'rtmp://', 'udp://', 'rtp://')):
                entries.append((pending, stream))
            pending = []
    if not entries:
        raise ValueError('No channel entries: ' + url)
    return entries

def main():
    output, seen, report = ['#EXTM3U'], set(), []
    for source in SOURCES:
        entries = read_source(source)
        added = 0
        for metadata, stream in entries:
            key = (stream, tuple(metadata[1:]))
            if key in seen:
                continue
            seen.add(key)
            output.extend(metadata + [stream])
            added += 1
        report.append({'source': source, 'entries': len(entries), 'added': added})
    Path('merged.m3u').write_text('\n'.join(output) + '\n', encoding='utf-8')
    Path('report.json').write_text(json.dumps({'entries': len(seen), 'sources': report}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
