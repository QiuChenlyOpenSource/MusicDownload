import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.zip.Inflater;

import static javax.crypto.Cipher.DECRYPT_MODE;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world!");
        String d = new String(unzip(readFileByBytes("/Users/qiuchenly/Downloads/response")));
        System.out.println(d);

        d = new String(unzip(readFileByBytes("/Users/qiuchenly/Downloads/request")));
        d = new String(hex2byte(d));
        byte[] bytes = hex2byte(d);
        d = new String(AesDecrypt(bytes, "6480fedae539deb2".getBytes()));
        System.out.println(d);
    }

    public static byte[] readFileByBytes(String fileName) {
        try {
            //传入文件路径fileName，底层实现 new FileInputStream(new File(fileName));相同
            FileInputStream in = new FileInputStream(fileName);
            //每次读10个字节，放到数组里
            byte[] bytes = new byte[1024];
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            int c;
            while ((c = in.read(bytes)) != -1) {
                byteArrayOutputStream.write(bytes, 0, c);
            }
            return byteArrayOutputStream.toByteArray();
        } catch (Exception e) {
            // TODO: handle exception
        }
        return new byte[0];
    }

    private static byte[] hex2byte(String str) {
        if (str == null || str.length() < 2) {
            return new byte[0];
        }
        String lowerCase = str.toLowerCase();
        int length = lowerCase.length() / 2;
        byte[] bArr = new byte[length];
        for (int i = 0; i < length; i++) {
            int i2 = i * 2;
            String key = lowerCase.substring(i2, i2 + 2);
            int b = Integer.parseInt(key, 16);
            int a = b & 255;
            bArr[i] = (byte) a;
        }
        return bArr;
    }

    public static byte[] AesEncrypt(byte[] bArr, byte[] key) {
        try {
            if (key.length != 16) {
                return null;
            }
            SecretKeySpec secretKeySpec = new SecretKeySpec(key, "AES");
            new IvParameterSpec(key);
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(1, secretKeySpec);
            try {
                return cipher.doFinal(bArr);
            } catch (Exception e) {
                System.out.println(e);
                return null;
            }
        } catch (Exception e2) {
            System.out.println(e2);
            return null;
        }
    }

    public static byte[] AesDecrypt(byte[] bArr, byte[] key) {
        try {
            if (key.length != 16) {
                return null;
            }
            SecretKeySpec secretKeySpec = new SecretKeySpec(key, "AES");
            new IvParameterSpec(key);
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(DECRYPT_MODE, secretKeySpec);
            try {
                return cipher.doFinal(bArr);
            } catch (Exception e) {
                System.out.println(e);
                return null;
            }
        } catch (Exception e2) {
            System.out.println(e2);
            return null;
        }
    }

    public static byte[] unzip(byte[] bArr) {
        Inflater inflater = new Inflater();
        inflater.reset();
        inflater.setInput(bArr);
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(bArr.length);
        try {
            byte[] bArr2 = new byte[1024];
            while (!inflater.finished()) {
                byteArrayOutputStream.write(bArr2, 0, inflater.inflate(bArr2));
            }
            bArr = byteArrayOutputStream.toByteArray();
            try {
                byteArrayOutputStream.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e2) {
            e2.printStackTrace();
        } catch (Throwable th) {
            try {
                byteArrayOutputStream.close();
            } catch (IOException e3) {
                e3.printStackTrace();
            }
            throw th;
        }
        inflater.end();
        return bArr;
    }
}