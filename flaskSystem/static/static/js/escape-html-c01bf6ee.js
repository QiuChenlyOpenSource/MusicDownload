import{g as e}from"./dayjs-4609adfa.js";
/*!
 * escape-html
 * Copyright(c) 2012-2013 TJ Holowaychuk
 * Copyright(c) 2015 Andreas Lubbe
 * Copyright(c) 2015 Tiancheng "Timothy" Gu
 * MIT Licensed
 */var a=/["'&<>]/;const r=e((function(e){var r,t=""+e,s=a.exec(t);if(!s)return t;var c="",n=0,o=0;for(n=s.index;n<t.length;n++){switch(t.charCodeAt(n)){case 34:r="&quot;";break;case 38:r="&amp;";break;case 39:r="&#39;";break;case 60:r="&lt;";break;case 62:r="&gt;";break;default:continue}o!==n&&(c+=t.substring(o,n)),o=n+1,c+=r}return o!==n?c+t.substring(o,n):c}));export{r as e};
