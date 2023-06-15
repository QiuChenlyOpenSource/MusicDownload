package DecompileFiles;

class main {
    public static void main(String[] args) {
        EncryptAndDecrypt.decryptAndSetCookie(EncryptAndDecrypt.TestCookie);
        System.out.println(Cookie.getCookie());
        System.out.println(getDeviceInfo());
    }

    public static device getDeviceInfo() {
        // DeviceInfo v10 = new DeviceInfo(
        // SystemInfoUtil.getUID(),
        // SystemInfoUtil.getSystemModel(),
        // SystemInfoUtil.getDeviceBrand(),
        // SystemInfoUtil.getAppVersionName(),
        // SystemInfoUtil.getSystemVersion(),
        // SystemInfoUtil.getAppVersionCode() + "",
        // null,
        // 0x40,
        // null);
        // {"appVersion":"7.1.2","deviceBrand":"360","deviceModel":"QK1707-A01","ip":"JmUXjTe5jZ739hq/SNt1JeTKEmxAXZsSxrJcQNvQxN-3wrP6LSd6//Wk2W4COwBVBEty0UQ8-/-KsjB\n3ekz/e09nw==","systemVersion":"1.7.2","uid":"822a3b85-a5c9-438e-a277-a8da412e8265","versionCode":"76"}
        String uid = "822a3b85-a5c9-438e-a277-a8da412e8265",
                systemVersion = "1.7.2",
                versionCode = "76",
                deviceBrand = "360",
                deviceModel = "QK1707-A01",
                appVersion = "7.1.2",
                encIP = "";
        device d = new device(uid, systemVersion, versionCode, deviceBrand, deviceModel, appVersion, encIP);
        encIP = EncryptAndDecrypt.encryptText(
                d.getEvalCode(),
                "F*ckYou!");
        d.setIP(encIP);
        return d;
    }
}

class device {
    public String uid = "822a3b85-a5c9-438e-a277-a8da412e8265",
            systemVersion = "1.7.2",
            versionCode = "76",
            deviceBrand = "360",
            deviceModel = "QK1707-A01",
            appVersion = "7.1.2",
            encIP = "";

    public device(String uid,
            String systemVersion,
            String versionCode,
            String deviceBrand,
            String deviceModel,
            String appVersion,
            String encIP) {
        this.uid = uid;
        this.systemVersion = systemVersion;
        this.versionCode = versionCode;
        this.deviceBrand = deviceBrand;
        this.deviceModel = deviceModel;
        this.appVersion = appVersion;
        this.encIP = encIP;
    }

    public void setIP(String ip) {
        this.encIP = ip;
    }

    public String getEvalCode() {
        return uid + deviceModel + deviceBrand + systemVersion + appVersion + versionCode;
    }
}
