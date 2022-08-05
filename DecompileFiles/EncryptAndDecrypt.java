package DecompileFiles;

import java.util.Calendar;
import java.util.List;
import java.util.Random;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/* loaded from: /Users/qiuchenly/Downloads/d.dex */
public class EncryptAndDecrypt {
    public static final String TestCookie = "1AxPKhgzRbWbIt8TfqfajraPgxZWmMhAoSh9HlWlPhFHQyVedFYNSOsPofZ/vj|J2XTtzdDIAqupT1T5tYMrN/u/qniED56dcBaUZSgXG2lN10Nc1OZIN87TsxcLwZQ1/TolMZ7f+oNiqQMPHs1Ff/Q==%aa2Ef93/cpOC3DyRvsNohA==";

    private static String GetFullNumber(int num) {
        if (num < 10) {
            return "00" + num;
        } else if (num < 100) {
            return "0" + num;
        } else {
            return num + "";
        }
    }

    private static char[] reverse(char[] clist) {
        for (int i = 0; i < clist.length / 2; i++) {
            char c = clist[(clist.length - i) - 1];
            clist[(clist.length - i) - 1] = clist[i];
            clist[i] = c;
        }
        return clist;
    }

    private static String arrToStr(char[] cArr) {
        String str = "";
        for (int i = 0; i < cArr.length; i++) {
            str = str + cArr[i];
        }
        return str;
    }

    private static String listToStr(List<Character> cList) {
        String str = "";
        for (int i = 0; i < cList.size(); i++) {
            str = str + cList.get(i);
        }
        return str;
    }

    public static String encryptDES(String text, String key) {
        try {
            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
            cipher.init(1, new SecretKeySpec(key.getBytes(), "DES"), new IvParameterSpec(key.getBytes()));
            return java.util.Base64.getEncoder().encodeToString(cipher.doFinal(text.getBytes())).trim();
        } catch (Exception e) {
            return e.getMessage();
        }
    }

    // ok
    public static String decryptDES(String text, String key) {
        if (text == null || key == null) {
            return null;
        }
        try {
            byte[] decode = java.util.Base64.getDecoder().decode(text);
            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
            cipher.init(2, new SecretKeySpec(key.getBytes(), "DES"), new IvParameterSpec(key.getBytes()));
            return new String(cipher.doFinal(decode), "utf-8");
        } catch (Exception e) {
            return e.getMessage();
        }
    }

    // ok
    public static boolean decryptAndSetCookie(String enStr) {
        String replace = enStr.replace("-", "").replace("|", "");
        if (replace.length() < 10 || !replace.contains("%")) {
            return false;
        }
        String[] split = replace.split("%");
        String str = split[0];
        String decryptDES = decryptDES(split[1], str.substring(0, 8));
        if (decryptDES.length() < 8) {
            decryptDES = decryptDES + "QMD";
        }
        Cookie.setCookie(decryptDES(str, decryptDES.substring(0, 8)), decryptDES);
        return true;
    }

    public static String encryptText(String text, String qq) {
        String key = ("QMD" + qq).substring(0, 8);
        StringBuilder sb = new StringBuilder(encryptDES(text, key));
        Random random = new Random((long) Calendar.getInstance().get(5));
        int nextInt = random.nextInt(4) + 1;
        for (int i = 0; i < nextInt; i++) {
            sb.insert(random.nextInt(sb.length()), "-");
        }
        return sb.toString();
    }

    public static String encryptText(String text) {
        return encryptText(text, Cookie.getQQ());
    }

    public static String decryptText(String text, String qq) {
        return decryptDES(text.replace("-", ""), ("QMD" + qq).substring(0, 8));
    }

    public static String decryptText(String text) {
        return decryptText(text, Cookie.getQQ());
    }
}