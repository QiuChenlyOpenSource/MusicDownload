package DecompileFiles;

public class Cookie {
    private static String Mkey;
    private static String QQ;

    // String Decryptor: 2 succeeded, 0 failed
    public static String getCookie() {
        return "qqmusic_key=[" + Cookie.Mkey + "];qqmusic_uin=[" + Cookie.QQ + "];";
    }

    public static String getMkey() {
        return Cookie.Mkey;
    }

    public static String getQQ() {
        return Cookie.QQ;
    }

    /**
     * 解密后的密钥保存
     * 
     * @param mkey
     * @param qq
     */
    public static void setCookie(String mkey, String qq) {
        Cookie.Mkey = mkey;
        Cookie.QQ = qq;
    }
}