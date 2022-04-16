// ==UserScript==
// @name         Better Zhihu
// @namespace    https://morningstar529.com
// @version      0.1
// @description  对知乎客户端做优化
// @author       Henry Ji
// @icon         https://cdn.jsdelivr.net/gh/HenryJi529/ImageHosting/202110292034373.png
// @include      https://www.zhihu.com/*
// @require      https://cdn.jsdelivr.net/npm/jquery@3.6/dist/jquery.min.js
// @grant        none
// ==/UserScript==

function getEl4xpath(xpath) {
	const pEl = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null)
	const result = []
	let dom = pEl.iterateNext()
	while (dom) {
		result.push(dom)
		dom = pEl.iterateNext()
	}
	return result
}

window.addEventListener('load', function () {
	// 清理推荐、热榜
	document.getElementsByClassName("TopstoryTabs Topstory-tabs")[0].style.display = "none";

	//背景修改
	try {
		getEl4xpath('/html/body/div[1]/div/main/div/div[1]')[0].style.display = "none";
	}
	catch (err) {
		console.log("not found")
	}

	// 清理顶部
	try {
		getEl4xpath('/html/body/div[1]/div/main/div/div[2]')[0].style.display = "none";
	}
	catch (err) {
		console.log("not found")
	}

	// 清理侧边
	try {
		document.getElementsByTagName("footer")[0].style.display = "none";
		getEl4xpath('/html/body/div[1]/div/main/div/div[3]/div[2]')[0].style.display = "none";
		document.getElementsByClassName("Topstory-container")[0].style.width = "100%";
		document.getElementsByClassName("Topstory-container")[0].style.maxWidth = "1500px"
		document.getElementsByClassName("Topstory-mainColumn")[0].style.width = "100%";
	}
	catch (err) {
		console.log("not found")
	}

	// 修改图标
	let favicon = document.querySelector('link[rel~="icon"]');
	let clone = favicon.cloneNode(!0);
	clone.href = "https://cdn.jsdelivr.net/gh/HenryJi529/ImageHosting/202110292034373.png"
	favicon.parentNode.removeChild(favicon);
	document.head.appendChild(clone);
}, false);