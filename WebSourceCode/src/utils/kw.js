function l(s) {
    return y(d(m(s), 8 * s.length))
}

function d(t, e) {
    t[e >> 5] |= 128 << 24 - e % 32,
        t[15 + (e + 64 >> 9 << 4)] = e;
    for (var n = Array(80), a = 1732584193, b = -271733879, o = -1732584194, r = 271733878, c = -1009589776, i = 0; i < t.length; i += 16) {
        for (var l = a, d = b, m = o, y = r, x = c, k = 0; k < 80; k++) {
            n[k] = k < 16 ? t[i + k] : h(n[k - 3] ^ n[k - 8] ^ n[k - 14] ^ n[k - 16], 1);
            var C = v(v(h(a, 5), f(k, b, o, r)), v(v(c, n[k]), w(k)));
            c = r,
                r = o,
                o = h(b, 30),
                b = a,
                a = C
        }
        a = v(a, l),
            b = v(b, d),
            o = v(o, m),
            r = v(r, y),
            c = v(c, x)
    }
    return Array(a, b, o, r, c)
}

function f(t, b, e, n) {
    return t < 20 ? b & e | ~b & n : t < 40 ? b ^ e ^ n : t < 60 ? b & e | b & n | e & n : b ^ e ^ n
}

function w(t) {
    return t < 20 ? 1518500249 : t < 40 ? 1859775393 : t < 60 ? -1894007588 : -899497514
}

function v(t, e) {
    var n = (65535 & t) + (65535 & e);
    return (t >> 16) + (e >> 16) + (n >> 16) << 16 | 65535 & n
}

function h(t, e) {
    return t << e | t >>> 32 - e
}

function m(t) {
    for (var e = Array(), i = 0; i < 8 * t.length; i += 8)
        e[i >> 5] |= (255 & t.charCodeAt(i / 8)) << 24 - i % 32;
    return e
}

function y(t) {
    for (var e = "0123456789abcdef", n = "", i = 0; i < 4 * t.length; i++)
        n += e.charAt(t[i >> 2] >> 8 * (3 - i % 4) + 4 & 15) + e.charAt(t[i >> 2] >> 8 * (3 - i % 4) & 15);
    return n
}

const enc = {}

function calc() {
    var r = function (e, t) {
        return e << t | e >>> 32 - t
    }
        , o = function (e, t) {
            var n, r, o, c, l;
            return o = 2147483648 & e,
                c = 2147483648 & t,
                l = (1073741823 & e) + (1073741823 & t),
                (n = 1073741824 & e) & (r = 1073741824 & t) ? 2147483648 ^ l ^ o ^ c : n | r ? 1073741824 & l ? 3221225472 ^ l ^ o ^ c : 1073741824 ^ l ^ o ^ c : l ^ o ^ c
        }
        , c = function (a, b, e, t, n, s, c) {
            return a = o(a, o(o(function (e, t, n) {
                return e & t | ~e & n
            }(b, e, t), n), c)),
                o(r(a, s), b)
        }
        , l = function (a, b, e, t, n, s, c) {
            return a = o(a, o(o(function (e, t, n) {
                return e & n | t & ~n
            }(b, e, t), n), c)),
                o(r(a, s), b)
        }
        , f = function (a, b, e, t, n, s, c) {
            return a = o(a, o(o(function (e, t, n) {
                return e ^ t ^ n
            }(b, e, t), n), c)),
                o(r(a, s), b)
        }
        , d = function (a, b, e, t, n, s, c) {
            return a = o(a, o(o(function (e, t, n) {
                return t ^ (e | ~n)
            }(b, e, t), n), c)),
                o(r(a, s), b)
        }
        , h = function (e) {
            var t, n = "", r = "";
            for (t = 0; t <= 3; t++)
                n += (r = "0" + (e >>> 8 * t & 255).toString(16)).substr(r.length - 2, 2);
            return n
        };
    enc.md5 = function (e) {
        var t, n, r, m, v, a, b, y, w, _ = Array();
        for (_ = function (e) {
            for (var t, n = e.length, r = n + 8, o = 16 * ((r - r % 64) / 64 + 1), c = Array(o - 1), l = 0, f = 0; f < n;)
                l = f % 4 * 8,
                    c[t = (f - f % 4) / 4] = c[t] | e.charCodeAt(f) << l,
                    f++;
            return l = f % 4 * 8,
                c[t = (f - f % 4) / 4] = c[t] | 128 << l,
                c[o - 2] = n << 3,
                c[o - 1] = n >>> 29,
                c
        }(e = function (e) {
            e = e.replace(/\x0d\x0a/g, "\n");
            for (var output = "", t = 0; t < e.length; t++) {
                var n = e.charCodeAt(t);
                n < 128 ? output += String.fromCharCode(n) : n > 127 && n < 2048 ? (output += String.fromCharCode(n >> 6 | 192),
                    output += String.fromCharCode(63 & n | 128)) : (output += String.fromCharCode(n >> 12 | 224),
                        output += String.fromCharCode(n >> 6 & 63 | 128),
                        output += String.fromCharCode(63 & n | 128))
            }
            return output
        }(e)),
            a = 1732584193,
            b = 4023233417,
            y = 2562383102,
            w = 271733878,
            t = 0; t < _.length; t += 16)
            n = a,
                r = b,
                m = y,
                v = w,
                a = c(a, b, y, w, _[t + 0], 7, 3614090360),
                w = c(w, a, b, y, _[t + 1], 12, 3905402710),
                y = c(y, w, a, b, _[t + 2], 17, 606105819),
                b = c(b, y, w, a, _[t + 3], 22, 3250441966),
                a = c(a, b, y, w, _[t + 4], 7, 4118548399),
                w = c(w, a, b, y, _[t + 5], 12, 1200080426),
                y = c(y, w, a, b, _[t + 6], 17, 2821735955),
                b = c(b, y, w, a, _[t + 7], 22, 4249261313),
                a = c(a, b, y, w, _[t + 8], 7, 1770035416),
                w = c(w, a, b, y, _[t + 9], 12, 2336552879),
                y = c(y, w, a, b, _[t + 10], 17, 4294925233),
                b = c(b, y, w, a, _[t + 11], 22, 2304563134),
                a = c(a, b, y, w, _[t + 12], 7, 1804603682),
                w = c(w, a, b, y, _[t + 13], 12, 4254626195),
                y = c(y, w, a, b, _[t + 14], 17, 2792965006),
                b = c(b, y, w, a, _[t + 15], 22, 1236535329),
                a = l(a, b, y, w, _[t + 1], 5, 4129170786),
                w = l(w, a, b, y, _[t + 6], 9, 3225465664),
                y = l(y, w, a, b, _[t + 11], 14, 643717713),
                b = l(b, y, w, a, _[t + 0], 20, 3921069994),
                a = l(a, b, y, w, _[t + 5], 5, 3593408605),
                w = l(w, a, b, y, _[t + 10], 9, 38016083),
                y = l(y, w, a, b, _[t + 15], 14, 3634488961),
                b = l(b, y, w, a, _[t + 4], 20, 3889429448),
                a = l(a, b, y, w, _[t + 9], 5, 568446438),
                w = l(w, a, b, y, _[t + 14], 9, 3275163606),
                y = l(y, w, a, b, _[t + 3], 14, 4107603335),
                b = l(b, y, w, a, _[t + 8], 20, 1163531501),
                a = l(a, b, y, w, _[t + 13], 5, 2850285829),
                w = l(w, a, b, y, _[t + 2], 9, 4243563512),
                y = l(y, w, a, b, _[t + 7], 14, 1735328473),
                b = l(b, y, w, a, _[t + 12], 20, 2368359562),
                a = f(a, b, y, w, _[t + 5], 4, 4294588738),
                w = f(w, a, b, y, _[t + 8], 11, 2272392833),
                y = f(y, w, a, b, _[t + 11], 16, 1839030562),
                b = f(b, y, w, a, _[t + 14], 23, 4259657740),
                a = f(a, b, y, w, _[t + 1], 4, 2763975236),
                w = f(w, a, b, y, _[t + 4], 11, 1272893353),
                y = f(y, w, a, b, _[t + 7], 16, 4139469664),
                b = f(b, y, w, a, _[t + 10], 23, 3200236656),
                a = f(a, b, y, w, _[t + 13], 4, 681279174),
                w = f(w, a, b, y, _[t + 0], 11, 3936430074),
                y = f(y, w, a, b, _[t + 3], 16, 3572445317),
                b = f(b, y, w, a, _[t + 6], 23, 76029189),
                a = f(a, b, y, w, _[t + 9], 4, 3654602809),
                w = f(w, a, b, y, _[t + 12], 11, 3873151461),
                y = f(y, w, a, b, _[t + 15], 16, 530742520),
                b = f(b, y, w, a, _[t + 2], 23, 3299628645),
                a = d(a, b, y, w, _[t + 0], 6, 4096336452),
                w = d(w, a, b, y, _[t + 7], 10, 1126891415),
                y = d(y, w, a, b, _[t + 14], 15, 2878612391),
                b = d(b, y, w, a, _[t + 5], 21, 4237533241),
                a = d(a, b, y, w, _[t + 12], 6, 1700485571),
                w = d(w, a, b, y, _[t + 3], 10, 2399980690),
                y = d(y, w, a, b, _[t + 10], 15, 4293915773),
                b = d(b, y, w, a, _[t + 1], 21, 2240044497),
                a = d(a, b, y, w, _[t + 8], 6, 1873313359),
                w = d(w, a, b, y, _[t + 15], 10, 4264355552),
                y = d(y, w, a, b, _[t + 6], 15, 2734768916),
                b = d(b, y, w, a, _[t + 13], 21, 1309151649),
                a = d(a, b, y, w, _[t + 4], 6, 4149444226),
                w = d(w, a, b, y, _[t + 11], 10, 3174756917),
                y = d(y, w, a, b, _[t + 2], 15, 718787259),
                b = d(b, y, w, a, _[t + 9], 21, 3951481745),
                a = o(a, n),
                b = o(b, r),
                y = o(y, m),
                w = o(w, v);
        return (h(a) + h(b) + h(y) + h(w)).toLowerCase()
    };
}

calc()

export default function EncToken(key = 'ERp7prxWCcmwwxs5msQ4fawshNixY7Qe') {
    return enc.md5(l(key)).toUpperCase()
}
// console.log(l('ERp7prxWCcmwwxs5msQ4fawshNixY7Qe'))
// console.log(enc.md5(l('ERp7prxWCcmwwxs5msQ4fawshNixY7Qe')).toUpperCase())