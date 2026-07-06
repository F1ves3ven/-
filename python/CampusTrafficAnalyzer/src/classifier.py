# classifier.py
# -*- coding: utf-8 -*-
"""
四川大学《计算机通信与网络》课程设计
模块：classifier.py (优化版：修复 80/443 误判 + 增强域名覆盖 + 智能兜底)
"""


class TrafficClassifier:
    def __init__(self):
        # 视频相关关键词（用于子域名/路径匹配）
        self.video_keywords = {
            "video", "vod", "live", "stream", "flv", "m3u8", "dash", "hls", "mp4", "playback",
            "pull", "push", "rtmp", "byteimg", "bytecdn", "douyincdn", "bilivideo",
            "ykimg", "iqiyipic", "hdslb", "biliapi", "toutiaocdn", "pstatp", "snssdk",
            "txmov2", "txvod", "myqcloud", "qcloud", "aliyuncs", "alicdn", "aliyunoss",
            "qiniucdn", "qiniudn", "clouddn", "ksyuncs", "kuaishouzt", "kwai", "kwai-pro",
            "googlevideo", "ytimg", "youtube", "netflix", "nflxvideo", "bilibili",
            "douyin", "iesdouyin", "tiktok", "tiktokv", "kuaishou", "ixigua", "xiguaapp",
            "haokan", "y.qq", "film", "tv", "movie", "episode", "series", "show", "anime",
            "cartoon", "drama", "variety", "music", "mv", "audio", "song", "playlist",
            "album", "singer", "band", "concert", "ktv", "radio", "fm", "podcast",
            "m4s", "ts", "f4v", "mpd", "webm", "3gp", "mov", "avi", "wmv", "rmvb", "mkv",
            "cdn", "img", "media", "cache", "download", "static", "akamaized",
            "p2p", "peer", "seed", "torrent", "bt", "ed2k",
        }

        # 根域名精确匹配表（大幅扩充）
        self.root_domains = {
            "学习办公": {
                "scu.edu.cn", "edu.cn", "tsinghua.edu.cn", "pku.edu.cn", "fudan.edu.cn",
                "zju.edu.cn", "sjtu.edu.cn", "ustc.edu.cn", "nju.edu.cn", "buaa.edu.cn",
                "github.com", "githubassets.com", "githubusercontent.com", "github.io",
                "raw.githubusercontent.com", "gist.github.com",
                "gitee.com", "gitcode.com", "coding.net", "gitlab.com", "git-scm.com",
                "csdn.net", "oschina.net", "juejin.cn", "segmentfault.com", "infoq.cn",
                "stackoverflow.com", "stackexchange.com", "superuser.com",
                "zhihu.com", "zhimg.com", "zhihuishu.com", "chaoxing.com",
                "microsoft.com", "office.com", "office365.com", "visualstudio.com",
                "live.com", "outlook.com", "hotmail.com", "msn.com",
                "wps.cn", "zoho.com", "feishu.cn", "larksuite.com", "dingtalk.com",
                "tencent.com", "qqmail.com", "exmail.qq.com", "mail.qq.com",
                "springer.com", "ieee.org", "acm.org", "cnki.net", "wanfangdata.com.cn",
                "sciencedirect.com", "researchgate.net", "arxiv.org", "arxiv-abs.com",
                "scholar.google.com", "webofscience.com", "pubmed.ncbi.nlm.nih.gov",
                "zoom.us", "zoom.com.cn", "teams.microsoft.com", "meeting.tencent.com",
                "class.tencent.com", "ke.qq.com", "xuetangx.com", "icourse163.org",
                "mooc.cn", "bilibili.com", "bilibili.cn", "b23.tv",
                "shimo.im", "yuque.com", "doc.weixin.qq.com", "docs.qq.com",
                "notion.so", "evernote.com", "youdao.com", "youdao.cn",
                "fanyi.baidu.com", "translate.google.com", "deepl.com", "papago.com",
                "processon.com", "draw.io", "diagrams.net", "app.diagrams.net",
                "baidu.com", "baike.baidu.com", "wenku.baidu.com", "zhidao.baidu.com",
                "pan.baidu.com", "tieba.baidu.com", "map.baidu.com", "jianshu.com",
                "juejin.cn", "juejin.im", "imooc.com", "runoob.com", "w3school.com.cn",
                "leetcode.cn", "leetcode.com", "luogu.com.cn", "nowcoder.com",
                "kaggle.com", "coursera.org", "edx.org", "udemy.com", "udacity.com",
                "bilibili.com", "bilibili.cn", "b23.tv", "acfun.cn", "niconico.jp",
                "youtube.com", "youtu.be", "googlevideo.com", "ytimg.com",
                "netflix.com", "nflxvideo.net", "nflxso.net", "hulu.com",
                "disneyplus.com", "primevideo.com", "hbo.com", "hbomax.com",
                "iqiyi.com", "iqiyipic.com", "youku.com", "ykimg.com",
                "tudou.com", "le.com", "letv.com", "mgtv.com", "hunantv.com",
                "pptv.com", "pptvcdn.com", "sohu.com", "mytvnet.tv",
                "v.qq.com", "film.qq.com", "video.qq.com", "tv.qq.com",
                "douyin.com", "iesdouyin.com", "douyincdn.com", "douyinpic.com",
                "tiktok.com", "tiktokcdn.com", "tiktokv.com",
                "kuaishou.com", "kuaishouzt.com", "kwai.com", "kwai-pro.com",
                "ixigua.com", "xiguaapp.com", "haokan.baidu.com", "baijiahao.baidu.com",
                "live.bilibili.com", "live.douyin.com", "live.kuaishou.com",
                "huya.com", "huyagame.cn", "douyu.com", "douyucdn.cn",
                "yy.com", "yycdn.com", "cc.163.com", "live.163.com",
                "twitch.tv", "ttvnw.net", "mixer.com",
                "music.163.com", "y.qq.com", "kuwo.cn", "kugou.com", "xiami.com",
                "spotify.com", "spotifycdn.com", "music.apple.com",
                "soundcloud.com", "podcast.apple.com", "ximalaya.com", "qingting.fm",
                "alicdn.com", "aliyun.com", "aliyuncdn.com", "aliyunoss.com",
                "aliyuncs.com", "tbcache.com", "tbcdn.cn",
                "myqcloud.com", "qcloud.com", "tencentcos.com", "tencent-cdn.com",
                "qiniudn.com", "qiniucdn.com", "clouddn.com", "qbox.me",
                "upaiyun.com", "upyun.com", "jcloud.com",
                "akamaized.net", "akamai.net", "cloudfront.net", "fastly.net",
                "byteimg.com", "bytedance.com", "pstatp.com", "toutiaocdn.com",
                "bdstatic.com", "bcebos.com", "baidubce.com", "bdimg.com",
                "txmov2.a.kwimgs.com", "txvod.a.kwimgs.com",
                "ksyuncs.com", "kuaishouzt.com",
                "googleusercontent.com", "gstatic.com",
                "weixin.qq.com", "wx.qq.com", "wechat.com", "wxapp.tc.qq.com",
                "qq.com", "ti.qq.com", "web.qq.com", "im.qq.com", "wx.qq.com",
                "weibo.com", "weibo.cn", "sinaimg.cn", "sina.com.cn", "sina.com",
                "xiaohongshu.com", "xhscdn.com", "xhslink.com",
                "twitter.com", "x.com", "twimg.com", "t.co",
                "facebook.com", "fbcdn.net", "instagram.com", "cdninstagram.com",
                "whatsapp.com", "wa.me", "telegram.org", "t.me", "telegram.me",
                "signal.org", "line.me", "line-apps.com", "kakao.com",
                "jianshu.com", "jianshu.io",
                "tieba.baidu.com", "reddit.com", "redditmedia.com",
                "quora.com", "discord.com", "discordapp.com", "discord.gg",
                "nga.cn", "nga.178.com", "v2ex.com", "hostloc.com",
                "soulapp.cn", "soulapp.me", "momo.com", "immomo.com",
                "tantanapp.com", "blued.com", "grindr.com", "tinder.com",
                "linkedin.com", "licdn.com", "maimai.cn",
                "game.qq.com", "qt.qq.com", "pvp.qq.com", "lol.qq.com",
                "cf.qq.com", "dnf.qq.com", "nz.qq.com", "codm.qq.com",
                "pubgmobile.com", "proximabeta.com", "garena.com",
                "tencentgames.com", "igame.qq.com",
                "game.163.com", "game.126.net", "163jiasu.com",
                "yys.163.com", "mhxy.163.com", "dhxy.163.com",
                "onmyoji.net", "identityv.com", "neteasegames.com",
                "mihoyo.com", "hoyoverse.com", "ys7.com", "bh3.com",
                "genshinimpact.com", "honkaistarrail.com", "zenlesszonezero.com",
                "steampowered.com", "steamcommunity.com", "steamcontent.com",
                "epicgames.com", "epicgamescdn.com", "unrealengine.com",
                "gog.com", "origin.com", "ea.com", "eaassets.com",
                "battlenet.com.cn", "blizzard.com", "blzstatic.cn",
                "ubisoft.com", "ubi.com", "rockstargames.com",
                "xboxlive.com", "xbox.com", "playstation.com", "playstation.net",
                "nintendo.com", "nintendo.net",
                "tap.io", "taptap.com", "taptapcdn.com",
                "9game.cn", "ali213.net", "3dmgame.com", "gamersky.com",
                "uu.163.com", "xunyou.com", "qiyou.cn", "golink.com",
                "huya.com", "douyu.com", "egame.qq.com",
                "microsoft.com", "windowsupdate.com", "update.microsoft.com",
                "apple.com", "icloud.com", "mzstatic.com", "apple-dns.net",
                "google.com", "googleapis.com", "googleusercontent.com", "gstatic.com",
                "android.com", "google-analytics.com", "googletagmanager.com",
                "xiaomi.com", "miui.com", "mi.com", "mi-fds.com",
                "huawei.com", "hicloud.com", "vmall.com", "dbankcdn.com",
                "oppo.com", "coloros.com", "realme.com", "vivo.com",
                "samsung.com", "samsungapps.com",
                "tencentcloud.com", "qcloud.com", "myqcloud.com", "tencentcos.com",
                "volces.com", "bytedance.com",
                "upaiyun.com", "upyun.com", "jcloud.com",
                "dns.google", "cloudflare.com", "cloudflare-dns.com",
                "quad9.net", "opendns.com", "dnspod.cn", "dnspod.com",
                "360.cn", "360.com", "360safe.com", "360totalsecurity.com",
                "geotrust.com", "digicert.com", "letsencrypt.org",
                "ntp.org", "pool.ntp.org", "time.windows.com",
                "firebase.google.com", "fcm.googleapis.com", "jpush.cn",
                "getui.com", "umeng.com", "umengcloud.com", "bugly.qq.com",
                "amap.com", "gaode.com", "map.baidu.com", "maps.google.com",
                "lbsyun.baidu.com",
                "taobao.com", "tmall.com", "tmall.hk", "alibaba.com",
                "1688.com", "jd.com", "360buyimg.com", "jdcdn.com",
                "pinduoduo.com", "yangkeduo.com", "suning.com",
                "vip.com", "vipshop.com", "dangdang.com",
                "amazon.com", "amazon.cn", "amazonaws.com",
                "ebay.com", "rakuten.co.jp", "shopee.com", "lazada.com",
                "alipay.com", "alipayobjects.com", "alipay-eco.com",
                "wx.tenpay.com", "pay.weixin.qq.com", "wechatpay.com",
                "unionpay.com", "95516.com", "chinaums.com",
                "meituan.com", "meituan.net", "dianping.com",
                "ele.me", "eleme.io",
                "sf-express.com", "zto.com", "yto.net.cn",
                "didiglobal.com", "didiaustralia.com.au", "xiaojukeji.com",
                "antfin.com", "antgroup.com", "mybank.cn",
                "icbc.com.cn", "ccb.com", "boc.cn", "abchina.com",
                "bankcomm.com", "cmbchina.com", "cmbchina.cn",
                "webank.com", "xinwangbank.com",
                "xueqiu.com", "eastmoney.com", "10jqka.com.cn",
            },
            "网络视频": {
                "bilibili.com", "bilivideo.com", "hdslb.com", "biliapi.net", "biliapi.com",
                "iqiyi.com", "iqiyipic.com", "iq.com", "youku.com", "ykimg.com",
                "tudou.com", "le.com", "letv.com", "mgtv.com", "hunantv.com",
                "pptv.com", "pptvcdn.com", "sohu.com", "mytvnet.tv",
                "v.qq.com", "film.qq.com", "video.qq.com", "tv.qq.com",
                "youtube.com", "youtu.be", "googlevideo.com", "ytimg.com", "youtubei.googleapis.com",
                "netflix.com", "nflxvideo.net", "nflxso.net", "nflxext.com", "hulu.com",
                "disneyplus.com", "primevideo.com", "hbo.com", "hbomax.com", "max.com",
                "douyin.com", "iesdouyin.com", "douyincdn.com", "douyinpic.com", "douyinstatic.com",
                "tiktok.com", "tiktokcdn.com", "tiktokv.com", "tiktokcdn-us.com", "musical.ly",
                "kuaishou.com", "kuaishouzt.com", "kwai.com", "kwai-pro.com", "kuaishoupay.com",
                "ixigua.com", "xiguaapp.com", "haokan.baidu.com", "baijiahao.baidu.com",
                "live.bilibili.com", "live.douyin.com", "live.kuaishou.com",
                "huya.com", "huyagame.cn", "douyu.com", "douyucdn.cn", "douyutv.com",
                "yy.com", "yycdn.com", "cc.163.com", "live.163.com",
                "twitch.tv", "ttvnw.net", "mixer.com", "streamlabs.com",
                "music.163.com", "y.qq.com", "kuwo.cn", "kugou.com", "xiami.com",
                "spotify.com", "spotifycdn.com", "music.apple.com", "itunes.apple.com",
                "soundcloud.com", "podcast.apple.com", "ximalaya.com", "qingting.fm", "fm.ximalaya.com",
                "alicdn.com", "aliyun.com", "aliyuncdn.com", "aliyunoss.com",
                "aliyuncs.com", "tbcache.com", "tbcdn.cn",
                "myqcloud.com", "qcloud.com", "tencentcos.com", "tencent-cdn.com",
                "qiniudn.com", "qiniucdn.com", "clouddn.com", "qbox.me",
                "upaiyun.com", "upyun.com", "jcloud.com",
                "akamaized.net", "akamai.net", "cloudfront.net", "fastly.net", "fastly.com",
                "byteimg.com", "bytedance.com", "byted-static.com", "pstatp.com", "toutiaocdn.com",
                "bdstatic.com", "bcebos.com", "baidubce.com", "bdimg.com", "bdgslb.com",
                "txmov2.a.kwimgs.com", "txvod.a.kwimgs.com",
                "ksyuncs.com", "kuaishouzt.com",
                "googleusercontent.com", "gstatic.com", "ggpht.com",
                "b23.tv", "acfun.cn", "niconico.jp", "nicovideo.jp", "dailymotion.com",
                "vimeo.com", "veoh.com", "metacafe.com", "break.com",
                "crunchyroll.com", "funimation.com", "vrvmusic.com",
                "tidal.com", "deezer.com", "pandora.com", "iheart.com",
                "napster.com", "bandcamp.com", "audiomack.com", "mixcloud.com",
            },
            "社交聊天": {
                "weixin.qq.com", "wx.qq.com", "wechat.com", "wxapp.tc.qq.com", "wechatpay.com",
                "qq.com", "ti.qq.com", "web.qq.com", "im.qq.com", "mobile.qq.com",
                "weibo.com", "weibo.cn", "sinaimg.cn", "sina.com.cn", "sina.com",
                "xiaohongshu.com", "xhscdn.com", "xhslink.com", "xhsapp.com",
                "twitter.com", "x.com", "twimg.com", "t.co", "tweetdeck.com",
                "facebook.com", "fbcdn.net", "instagram.com", "cdninstagram.com", "igcdn.com",
                "whatsapp.com", "wa.me", "telegram.org", "t.me", "telegram.me", "telegram-cdn.org",
                "signal.org", "signal.chat", "line.me", "line-apps.com", "line-scdn.net", "kakao.com",
                "jianshu.com", "jianshu.io",
                "tieba.baidu.com", "reddit.com", "redditmedia.com", "redd.it", "redditstatic.com",
                "quora.com", "discord.com", "discordapp.com", "discord.gg", "discord.media",
                "nga.cn", "nga.178.com", "v2ex.com", "hostloc.com",
                "soulapp.cn", "soulapp.me", "momo.com", "immomo.com",
                "tantanapp.com", "blued.com", "grindr.com", "tinder.com", "badoo.com",
                "linkedin.com", "licdn.com", "maimai.cn", "maimai.com",
                "snapchat.com", "sc-cdn.net", "pinterest.com", "pinimg.com",
                "tumblr.com", "tmblr.com", "flickr.com", "staticflickr.com",
                "vk.com", "vk.me", "vkuser.net", "ok.ru", "odnoklassniki.ru",
                "wechat.com", "weixin.com", "qq.com", "qzone.qq.com", "t.qq.com",
            },
            "休闲游戏": {
                "game.qq.com", "qt.qq.com", "pvp.qq.com", "lol.qq.com",
                "cf.qq.com", "dnf.qq.com", "nz.qq.com", "codm.qq.com", "cod.qq.com",
                "pubgmobile.com", "proximabeta.com", "garena.com", "garenanow.com",
                "tencentgames.com", "igame.qq.com", "gamecenter.qq.com",
                "game.163.com", "game.126.net", "163jiasu.com",
                "yys.163.com", "mhxy.163.com", "dhxy.163.com",
                "onmyoji.net", "identityv.com", "neteasegames.com",
                "mihoyo.com", "hoyoverse.com", "ys7.com", "bh3.com",
                "genshinimpact.com", "honkaistarrail.com", "zenlesszonezero.com",
                "steampowered.com", "steamcommunity.com", "steamcontent.com", "steamgames.com",
                "epicgames.com", "epicgamescdn.com", "unrealengine.com", "unrealtournament.com",
                "gog.com", "origin.com", "ea.com", "eaassets.com", "eacdn.com", "eastore.com",
                "battlenet.com.cn", "blizzard.com", "blzstatic.cn", "battle.net",
                "ubisoft.com", "ubi.com", "rockstargames.com", "rockstarnetwork.com",
                "xboxlive.com", "xbox.com", "playstation.com", "playstation.net", "sonyentertainmentnetwork.com",
                "nintendo.com", "nintendo.net", "nintendo.co.jp",
                "tap.io", "taptap.com", "taptapcdn.com", "taptapdada.com",
                "9game.cn", "ali213.net", "3dmgame.com", "gamersky.com", "ali213.com",
                "uu.163.com", "xunyou.com", "qiyou.cn", "golink.com", "golinkapi.com",
                "huya.com", "douyu.com", "egame.qq.com", "egame.qq.com",
                "roblox.com", "rbxcdn.com", "minecraft.net", "mojang.com",
                "fortnite.com", "unrealengine.com", "pubg.com", "bluehole.net",
                "activision.com", "callofduty.com", "crashbandicoot.com",
                "bethesda.net", "zenimax.com", "idsoftware.com",
                "valvesoftware.com", "valve.net", "dota2.com", "csgo.com", "counter-strike.net",
                "leagueoflegends.com", "riotgames.com", "wildrift.com", "valorant.com",
                "overwatch.com", "hearthstone.com", "worldofwarcraft.com", "starcraft.com",
                "diablo.com", "heroesofthestorm.com", "warcraft.com",
            },
            "系统服务": {
                "microsoft.com", "windowsupdate.com", "update.microsoft.com", "windows.com",
                "apple.com", "icloud.com", "mzstatic.com", "apple-dns.net", "me.com",
                "google.com", "googleapis.com", "googleusercontent.com", "gstatic.com",
                "android.com", "google-analytics.com", "googletagmanager.com", "googleadservices.com",
                "doubleclick.net", "googlesyndication.com", "googleoptimize.com",
                "xiaomi.com", "miui.com", "mi.com", "mi-fds.com", "mi-img.com",
                "huawei.com", "hicloud.com", "vmall.com", "dbankcdn.com", "hihonor.com",
                "oppo.com", "coloros.com", "realme.com", "vivo.com", "vivoglobal.com",
                "samsung.com", "samsungapps.com", "samsungdm.com", "samsungosp.com",
                "tencentcloud.com", "qcloud.com", "myqcloud.com", "tencentcos.com",
                "volces.com", "bytedance.com", "byted-static.com",
                "upaiyun.com", "upyun.com", "jcloud.com",
                "dns.google", "cloudflare.com", "cloudflare-dns.com", "cloudflare.net",
                "quad9.net", "opendns.com", "dnspod.cn", "dnspod.com", "dnspod.net",
                "360.cn", "360.com", "360safe.com", "360totalsecurity.com", "360webcache.com",
                "geotrust.com", "digicert.com", "letsencrypt.org", "symantec.com", "symcd.com",
                "verisign.com", "thawte.com", "globalsign.com", "entrust.net", "comodo.com",
                "ntp.org", "pool.ntp.org", "time.windows.com", "time.apple.com", "time.google.com",
                "firebase.google.com", "fcm.googleapis.com", "jpush.cn", "jiguang.cn",
                "getui.com", "umeng.com", "umengcloud.com", "bugly.qq.com", "tinkerpatch.com",
                "amap.com", "gaode.com", "map.baidu.com", "maps.google.com", "maps.googleapis.com",
                "lbsyun.baidu.com", "location.services.mozilla.com",
                "crashlytics.com", "fabric.io", "app-measurement.com", "google-analytics.com",
                "googleusercontent.com", "ggpht.com", "googlevideo.com",
                "msedge.net", "msftconnecttest.com", "msftncsi.com", "windows.com",
                "live.com", "msn.com", "bing.com", "outlook.com", "hotmail.com",
                "office.com", "office365.com", "microsoftonline.com", "login.microsoftonline.com",
                "sharepoint.com", "onedrive.com", "skype.com", "teams.microsoft.com",
                "aadrm.com", "azurerms.com", "protection.outlook.com",
                "apple-dns.net", "push-apple.com.akadns.net", "courier-push-apple.com.akadns.net",
                "icloud-content.com", "me.com", "mac.com", "itunes.com", "mzstatic.com",
                "akamaiedge.net", "akamaitechnologies.com", "edgekey.net", "edgesuite.net",
                "level3.net", "lithium.com", "cloudflare.net", "cloudflare.com", "fastly.com",
            },
            "购物金融": {
                "taobao.com", "tmall.com", "tmall.hk", "alibaba.com", "1688.com",
                "jd.com", "360buyimg.com", "jdcdn.com", "jdcloud.com", "jdpay.com",
                "pinduoduo.com", "yangkeduo.com", "pddcdn.com", "pddpic.com",
                "suning.com", "suningcdn.com", "vip.com", "vipshop.com", "dangdang.com",
                "amazon.com", "amazon.cn", "amazonaws.com", "amazon-adsystem.com",
                "ebay.com", "ebaystatic.com", "ebayimg.com", "rakuten.co.jp", "shopee.com", "lazada.com",
                "alipay.com", "alipayobjects.com", "alipay-eco.com", "alipaydev.com",
                "wx.tenpay.com", "pay.weixin.qq.com", "wechatpay.com", "tenpay.com",
                "unionpay.com", "95516.com", "chinaums.com", "qpay.qq.com",
                "meituan.com", "meituan.net", "dianping.com", "maoyan.com",
                "ele.me", "eleme.io", "ele.me", "ele.to",
                "sf-express.com", "zto.com", "yto.net.cn", "sto.cn", "best.com.cn",
                "didiglobal.com", "didiaustralia.com.au", "xiaojukeji.com", "didiglobal.com",
                "antfin.com", "antgroup.com", "mybank.cn", "antfortune.com",
                "icbc.com.cn", "ccb.com", "boc.cn", "abchina.com", "bankcomm.com",
                "cmbchina.com", "cmbchina.cn", "cmbchina.com", "cmbchina.net",
                "webank.com", "xinwangbank.com", "mybank.cn", "fudian-bank.com",
                "xueqiu.com", "eastmoney.com", "10jqka.com.cn", "hexun.com", "cs.com.cn",
                "fund.eastmoney.com", "stock.finance.sina.com.cn", "finance.qq.com",
            }
        }

        # Umbrella 域名映射
        self.umbrella_domains = {
            "qq.com": "TENCENT", "myqcloud.com": "TENCENT", "qcloud.com": "TENCENT",
            "tencent.com": "TENCENT", "tencent-cloud.net": "TENCENT", "wechat.com": "TENCENT",
            "weixin.qq.com": "TENCENT", "tencentgames.com": "TENCENT", "igame.qq.com": "TENCENT",
            "snssdk.com": "BYTEDANCE", "pstatp.com": "BYTEDANCE", "volces.com": "BYTEDANCE",
            "bytedance.com": "BYTEDANCE", "douyin.com": "BYTEDANCE", "iesdouyin.com": "BYTEDANCE",
            "tiktok.com": "BYTEDANCE", "tiktokv.com": "BYTEDANCE", "feishu.cn": "BYTEDANCE",
            "larksuite.com": "BYTEDANCE", "toutiao.com": "BYTEDANCE", "toutiaocdn.com": "BYTEDANCE",
            "byted-static.com": "BYTEDANCE",
            "163.com": "NETEASE", "126.net": "NETEASE", "127.net": "NETEASE",
            "netease.com": "NETEASE", "neteasegames.com": "NETEASE", "youdao.com": "NETEASE",
            "lofter.com": "NETEASE",
            "baidu.com": "BAIDU", "bdstatic.com": "BAIDU", "bcebos.com": "BAIDU",
            "baidubce.com": "BAIDU", "bdimg.com": "BAIDU", "bdgslb.com": "BAIDU",
            "taobao.com": "ALIBABA", "tmall.com": "ALIBABA", "alicdn.com": "ALIBABA",
            "alibaba.com": "ALIBABA", "aliyun.com": "ALIBABA", "aliyuncs.com": "ALIBABA",
            "alipay.com": "ALIBABA", "alipayobjects.com": "ALIBABA", "1688.com": "ALIBABA",
            "fliggy.com": "ALIBABA", "xiami.com": "ALIBABA", "dingtalk.com": "ALIBABA",
            "kuaishou.com": "KUAISHOU", "kuaishouzt.com": "KUAISHOU", "kwai.com": "KUAISHOU",
            "kwai-pro.com": "KUAISHOU",
        }

        # 端口映射：80/443 不再归为系统服务！
        self.port_category = {
            53: "系统服务", 123: "系统服务", 161: "系统服务",
            22: "系统服务", 23: "系统服务", 21: "系统服务",
            1935: "网络视频", 3478: "社交聊天", 5349: "社交聊天",
            8801: "学习办公", 8802: "学习办公",
            4000: "社交聊天", 4010: "休闲游戏", 10000: "社交聊天",
            27015: "休闲游戏", 27016: "休闲游戏", 27017: "休闲游戏",
            5060: "社交聊天", 5061: "社交聊天",
            # 80/443 不再预设，留给域名/关键词判断
        }

        # 关键词映射（用于无法识别域名时的兜底）
        self.keyword_rules = {
            "网络视频": [
                "video", "vod", "live", "stream", "flv", "m3u8", "dash", "hls", "mp4", "playback",
                "tv", "movie", "film", "episode", "anime", "cartoon", "drama", "variety",
                "music", "mv", "audio", "song", "playlist", "album", "singer", "concert", "ktv", "radio", "fm", "podcast",
                "bilibili", "youtube", "douyin", "tiktok", "kuaishou", "ixigua", "youku", "iqiyi",
                "netflix", "hulu", "disney", "hbo", "primevideo", "twitch", "vimeo",
                "m4s", "ts", "f4v", "mpd", "webm", "3gp", "mov", "avi", "wmv", "rmvb", "mkv",
                "akamaized", "cloudfront", "fastly", "byteimg", "pstatp", "toutiaocdn",
            ],
            "休闲游戏": [
                "game", "play", "pvp", "lol", "steam", "epic", "blizzard", "battlenet", "xbox", "playstation", "nintendo",
                "cheat", "hack", "mod", "save", "guild", "clan", "arena", "match", "rank", "score",
                "mihoyo", "hoyoverse", "genshin", "honkai", "zenless", "pubg", "fortnite", "valorant",
                "overwatch", "warcraft", "diablo", "hearthstone", "starcraft", "dota", "csgo", "counter-strike",
                "roblox", "minecraft", "mojang",
            ],
            "社交聊天": [
                "chat", "im", "message", "talk", "voice", "call", "social", "community", "forum",
                "weibo", "twitter", "facebook", "instagram", "whatsapp", "telegram", "snapchat",
                "discord", "reddit", "quora", "tieba", "sina", "tencent", "qq", "wechat", "weixin",
                "xiaohongshu", "linkedin", "tinder", "soul", "momo", "blued",
            ],
            "学习办公": [
                "learn", "study", "edu", "course", "class", "lesson", "homework", "exam", "test", "quiz",
                "library", "paper", "thesis", "journal", "academic", "research", "scholar", "mooc", "school", "campus",
                "github", "gitlab", "gitee", "csdn", "juejin", "stackoverflow", "zhihu", "bilibili",
                "office", "doc", "pdf", "slide", "ppt", "excel", "word", "notion", "wiki",
                "mail", "email", "outlook", "smtp", "imap", "pop3",
            ],
            "购物金融": [
                "shop", "buy", "mall", "store", "pay", "order", "cart", "coupon", "discount", "price", "sale",
                "taobao", "tmall", "jd", "amazon", "alipay", "wechatpay", "bank", "finance", "stock", "fund", "insurance", "loan",
                "credit", "debit", "wallet", "cash", "money", "gold", "silver", "crypto", "bitcoin",
            ],
            "系统服务": [
                "update", "upgrade", "patch", "sync", "backup", "cloud", "cdn", "dns", "ntp", "ocsp", "crl",
                "cert", "ssl", "tls", "api", "push", "analytics", "track", "ping", "probe", "health", "monitor",
                "windowsupdate", "microsoft", "apple", "google", "android", "firebase", "crashlytics",
                "google-analytics", "googletagmanager", "doubleclick", "googleadservices",
            ]
        }

    def _is_video_subdomain(self, host_lower: str) -> bool:
        parts = host_lower.split('.')
        for part in parts:
            if part in self.video_keywords:
                return True
        if any(k in host_lower for k in ["pull-", "push-", "live-", "vod-", "stream-", "video-", "flv-", "hls-", "dash-", "m4s-", "ts-"]):
            return True
        return False

    def classify_umbrella_traffic(self, vendor: str, host_lower: str, proto: str, size: int, dst_port: int = 0) -> str:
        if self._is_video_subdomain(host_lower):
            return "网络视频"

        if vendor == "TENCENT":
            if proto in ["UDP", "QUIC"] and size > 1000:
                return "网络视频"
            if any(k in host_lower for k in ["game", "tgpa", "speed", "pvp", "lol", "cf", "dnf", "codm", "cod", "pubg"]):
                return "休闲游戏"
            if any(k in host_lower for k in ["mail", "work", "doc", "exmail", "office", "meeting", "class", "ke", "edu"]):
                return "学习办公"
            if any(k in host_lower for k in ["wechat", "weixin", "im", "qq", "ti", "qzone", "tencent"]):
                return "社交聊天"
            if any(k in host_lower for k in ["video", "film", "tv", "live", "vod", "stream", "bilibili", "douyu", "huya"]):
                return "网络视频"
            return "其他流量"

        elif vendor == "BYTEDANCE":
            if any(k in host_lower for k in ["feishu", "lark", "larksuite"]):
                return "学习办公"
            if proto in ["UDP", "QUIC"] and size > 1200:
                return "网络视频"
            if any(k in host_lower for k in ["douyin", "tiktok", "iesdouyin", "video", "live", "vod"]):
                return "网络视频"
            if any(k in host_lower for k in ["toutiao", "news", "article"]):
                return "社交聊天"
            return "社交聊天"

        elif vendor == "NETEASE":
            if any(k in host_lower for k in ["mail", "email", "163.com", "126.com"]):
                return "学习办公"
            if any(k in host_lower for k in ["game", "yys", "mhxy", "onmyoji", "identityv", "neteasegames", "blizzard"]):
                return "休闲游戏"
            if any(k in host_lower for k in ["youdao", "dict", "translate", "note", "music", "cloudmusic"]):
                return "学习办公"
            if any(k in host_lower for k in ["video", "live", "vod", "stream", "bilibili"]):
                return "网络视频"
            return "其他流量"

        elif vendor == "BAIDU":
            if any(k in host_lower for k in ["map", "pan", "wenku", "tieba", "baike", "fanyi", "zhidao"]):
                return "学习办公"
            if any(k in host_lower for k in ["video", "haokan", "live"]):
                return "网络视频"
            return "其他流量"

        elif vendor == "ALIBABA":
            if any(k in host_lower for k in ["taobao", "tmall", "1688", "alipay", "fliggy", "ele", "meituan"]):
                return "购物金融"
            if any(k in host_lower for k in ["dingtalk", "ding", "docs", "xiami", "music", "video"]):
                return "学习办公"
            return "其他流量"

        elif vendor == "KUAISHOU":
            if any(k in host_lower for k in ["video", "live", "vod", "stream"]):
                return "网络视频"
            return "社交聊天"

        return "其他流量"

    def _keyword_classify(self, host_lower: str) -> str:
        """基于关键词的兜底分类"""
        for category, keywords in self.keyword_rules.items():
            for kw in keywords:
                if kw in host_lower:
                    return category
        return None

    def classify(self, host: str, proto: str = "TCP", size: int = 0, dst_port: int = 0, src_port: int = 0, video_hint: bool = False) -> str:
        if video_hint:
            return "网络视频"

        if not host:
            return self._classify_by_port(dst_port, src_port)

        host_lower = host.lower().strip()
        if host_lower in ["unknown", "", "none"]:
            return self._classify_by_port(dst_port, src_port)

        # 1. 视频子域名快速判断
        if self._is_video_subdomain(host_lower):
            return "网络视频"

        # 2. 根域名精确匹配
        parts = host_lower.split('.')
        for i in range(len(parts)):
            sub_domain = ".".join(parts[i:])
            for category, root_set in self.root_domains.items():
                if sub_domain in root_set:
                    return category

        # 3. Umbrella 域名匹配
        for i in range(len(parts)):
            sub_domain = ".".join(parts[i:])
            if sub_domain in self.umbrella_domains:
                vendor = self.umbrella_domains[sub_domain]
                return self.classify_umbrella_traffic(vendor, host_lower, proto, size, dst_port)

        # 4. 关键词兜底匹配
        keyword_result = self._keyword_classify(host_lower)
        if keyword_result:
            return keyword_result

        # 5. 协议+大小启发式判断
        if proto in ["UDP", "QUIC"]:
            if size > 1200:
                return "网络视频"
            elif size < 200:
                return "社交聊天"

        # 6. 端口兜底（80/443 不再预设为系统服务）
        return self._classify_by_port(dst_port, src_port)

    def _classify_by_port(self, dst_port: int, src_port: int) -> str:
        for port in [dst_port, src_port]:
            if port in self.port_category:
                return self.port_category[port]
        # 80/443 以及未知端口不再默认系统服务
        return "其他流量"

    def generate_user_profile(self, ip_stats: dict) -> str:
        total = ip_stats.get("total_bytes", 0)
        if total == 0:
            return "🏷️ 资产状态: 静默资产 (无活跃流量)"

        categories = ["学习办公", "网络视频", "社交聊天", "休闲游戏", "系统服务", "购物金融", "其他流量"]
        ratios = {}
        for cat in categories:
            ratios[cat] = ip_stats.get(cat, {}).get("bytes", 0) / total

        behavior_tags = []

        if ratios.get("学习办公", 0) > 0.35: behavior_tags.append("科研学霸 📚")
        if ratios.get("网络视频", 0) > 0.45: behavior_tags.append("追剧达人 🎬")
        if ratios.get("休闲游戏", 0) > 0.20: behavior_tags.append("极客玩家 🎮")
        if ratios.get("社交聊天", 0) > 0.35: behavior_tags.append("社交达人 💬")
        if ratios.get("购物金融", 0) > 0.25: behavior_tags.append("网购达人 🛒")
        if ratios.get("系统服务", 0) > 0.50: behavior_tags.append("系统后台 🔄")

        if ratios.get("学习办公", 0) > 0.20 and ratios.get("网络视频", 0) > 0.20:
            behavior_tags.append("劳逸结合 ⚖️")
        if ratios.get("休闲游戏", 0) > 0.15 and ratios.get("网络视频", 0) > 0.15:
            behavior_tags.append("娱乐至上 🎉")

        if not behavior_tags:
            behavior_tags.append("普通上网行为 🌐")

        profile_str = " | ".join(behavior_tags)
        return f"【终端标签】: {profile_str}"