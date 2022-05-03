## yt-dlp-iceberg

This is a project for managing and automating for the archiving of resources on the internet which are supported by yt-dlp.

### Configuration

See [sample_config.yaml](sample_config.yaml) which includes comments.


### Caveats:

#### Not all yt-dlp targets support archival.

In particular, your resource needs to be a list of videos, eg. a YouTube playlist or channel.

#### IP address reputation considerations

Yt-dlp on feeds/playlists typically has you making tons of API calls / fake browser requests to the website you're trying to archive from. If your archive intervals are too short, or you have tons of archive targets, you might look like a malicious robot to these services, and your IP might be blocked / rate limited. If you run into problems, consider utilizing a VPN service (Eg. Warp, Mullvad, etc), perhaps in combination with something like [wireproxy](https://github.com/octeep/wireproxy) that exposes a VPN as a regular proxy server.

#### Not parallel

By default, this does not download files or projects in parallel. You may be interested in using https://github.com/tuxlovesyou/squid-dl to speed up initial downloads (by setting the config variable `ytdlp_exec` to the squid-dl executable).