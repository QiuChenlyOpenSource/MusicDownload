this.f3212_GetMusicUtils1.getMusic(1, this.qqMid, GetMusicUtils.Type.f130qq, str4);
 public static final String f130qq = "qq";

 public void m4150_1$(int i, String str, String str2) {
        String str3 = this.f3213_qmd1.mo2398(C1452.cookie, str2)[0];
        String str4 = GetMusicUtils.Tone.mp3;
        if (i != 0 && i != 1) {
            str4 = i == 2 ? GetMusicUtils.Tone._320kmp3 : i == 3 ? GetMusicUtils.Tone.f129sq : "";
        }
        this.f3212_GetMusicUtils1.mo3080(1, this.qqMid, GetMusicUtils.Type.f130qq, str4);
    }
   public static final String _320kmp3 = "320kmp3";

        /* renamed from: hq */
        public static final String f127hq = "hq";

        /* renamed from: hr */
        public static final String f128hr = "hr";
        public static final String mp3 = "mp3";

        /* renamed from: sq */
        public static final String f129sq = "sq";

public static String byteToHexString(byte[] arr_b) {
        StringBuffer stringBuffer0 = new StringBuffer();
        int v;
        for(v = 0; v < arr_b.length; ++v) {
            String s = Integer.toHexString(arr_b[v]).toUpperCase();
            if(s.length() > 3) {
                stringBuffer0.append(s.substring(6));
            }
            else if(s.length() < 2) {
                stringBuffer0.append("0" + s);
            }
            else {
                stringBuffer0.append(s);
            }
        }

        return stringBuffer0.toString();
    }

public static void getMusic(String s, String s1, String s2, Callback getMusicUtils$Callback0) {
        String s3 = Build.MODEL;
        int v = Build.VERSION.SDK_INT;
        String s4 = System.currentTimeMillis() / 1000L + "";
        String s5 = GetMusicUtils.md5("f389249d91bd845c9b817db984054cfb" + s4 + "6562653262383463363633646364306534333663").toLowerCase();
        String s6 = "{\\\"method\\\":\\\"GetMusicUrl\\\",\\\"platform\\\":\\\"" + s1 + "\\\",\\\"t1\\\":\\\"" + s + "\\\",\\\"t2\\\":\\\"" + s2 + "\\\"}";
        String s7 = "{\\\"uid\\\":\\\"\\\",\\\"token\\\":\\\"\\\",\\\"deviceid\\\":\\\"84c599d711066ef740eb49109dac9782\\\",\\\"appVersion\\\":\\\"4.1.0.V4\\\",\\\"vercode\\\":\\\"4100\\\",\\\"device\\\":\\\"" + s3 + "\\\",\\\"osVersion\\\":\\\"" + v + "\\\"}";
        String s8 = "{\n\t\"text_1\":\t\"" + s6 + "\",\n\t\"text_2\":\t\"" + s7 + "\",\n\t\"sign_1\":\t\"" + s5 + "\",\n\t\"time\":\t\"" + s4 + "\",\n\t\"sign_2\":\t\"" + GetMusicUtils.md5(s6.replace("\\", "") + s7.replace("\\", "") + s5 + s4 + "NDRjZGIzNzliNzEx").toLowerCase() + "\"\n}";
        Log.d("GetMusicUtils", s8);
        String s9 = new String[]{"http://app.kzti.top:1030/client/cgi-bin/api.fcg", "http://119.91.134.171:1030/client/cgi-bin/api.fcg"}[new Random().nextInt(2)];
        Log.d("GetMusicUtils", "getMusic: " + s9);
        new Thread(() -> {
            String s1 = new String(GetMusicUtils.unzip(new Request().url(s9).post().header("Connection", "Keep-Alive").header("Content-Type", "gcsp/stream").header("Accept-Encoding", "gzip").contentByte(GetMusicUtils.gzip(GetMusicUtils.byteToHexString(GetMusicUtils.byteToHexString(GetMusicUtils.AesEncrypt(s8.getBytes(), "6480fedae539deb2".getBytes())).getBytes()).getBytes())).exec().body().bytes()));
            new Handler(Looper.getMainLooper()).post(() -> try {
                Log.d("GetMusicUtils", "getMusic: " + s1);
                getMusicUtils$Callback0.onMusicUrl(new JSONObject(s1).getString("data"));
            }
            catch(Exception exception0) {
                exception0.printStackTrace();
                getMusicUtils$Callback0.onMusicUrl("");
            });
        }).start();
    }

     public static byte[] AesEncrypt(byte[] bArr, byte[] bArr2) {
        try {
            if (bArr2.length != 16) {
                return null;
            }
            SecretKeySpec secretKeySpec = new SecretKeySpec(bArr2, "AES");
            new IvParameterSpec(bArr2);
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(1, secretKeySpec);
            try {
                return cipher.doFinal(bArr);
            } catch (Exception e) {
                System.out.println(e.toString());
                return null;
            }
        } catch (Exception e2) {
            System.out.println(e2.toString());
            return null;
        }
    }


     public static /* synthetic */ void lambda$getMusic$3(String str, byte[] bArr, final Callback callback) {
        final String str2 = new String(unzip(new HttpUtils.Request().url(str).post().header(HttpHeaders.HEAD_KEY_CONNECTION, "Keep-Alive")
        .header(HttpHeaders.HEAD_KEY_CONTENT_TYPE, "gcsp/stream")
        .header(HttpHeaders.HEAD_KEY_ACCEPT_ENCODING, "gzip")
        .contentByte(bArr)
        .exec()
        .body()
        .bytes()));
        new Handler(Looper.getMainLooper()).post(new Runnable() { // from class: com.e4a.runtime.components.impl.android.啾啾_GetMusicUtils类库.-$$Lambda$GetMusicUtils$ReMB7S0rzNwgvDlph_pGjbelpBU
            @Override // java.lang.Runnable
            public final void run() {
                GetMusicUtils.lambda$null$2(str2, callback);
            }
        });
    }