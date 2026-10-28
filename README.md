# Global and Hong Kong IPTV merger

Subscription URL, available only after the first successful workflow run:

https://raw.githubusercontent.com/AChan1004/iptv-merged/main/merged.m3u

The four sources are listed in SOURCES in merge.py. Hong Kong sources run first, followed by the IPTV-org global index. Alternative country/language versions of the global index are intentionally excluded.

Updates run on configuration pushes, manually in Actions, and daily at 22:00 UTC (06:00 Hong Kong time). Scheduled runs can be delayed or disabled under GitHub inactivity policies.

Every source must download and parse successfully before any output is published. On failure the last committed output is retained. Initial failure means the subscription does not yet exist. Check Actions logs for errors.

Deduplication uses the exact stream URL and auxiliary options, keeping the first channel metadata. Different URLs for the same named channel remain. Report counts are playlist entries, not unique TV stations. Relative URLs are resolved and per-channel options preserved. Source header attributes, including EPG URLs, are not merged; configure EPG separately. Player support varies.

This does not test playback, guarantee uptime or cover all IPTV services. Only access and redistribute streams you are authorized to use. Public sharing does not establish licensing. Never add passwords, private subscription URLs or tokens to this public repository.
