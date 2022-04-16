function startTimer() {
	delayTime = Number(sessionStorage.getItem('remainTime')) || 300;
	sendButton.value = delayTime.toString();
	sendButton.classList.add("btn-secondary");
	sendButton.classList.remove("btn-info");
	sendButton.setAttribute('disabled', 'disabled');
	let intervalID = setInterval(() => {
		sendButton.value = (Number(sendButton.value) - 1).toString();
		sessionStorage.setItem("remainTime", sendButton.value);
	}, 1000);
	setTimeout(() => {
		clearInterval(intervalID);
		sendButton.value = "获取"
		sendButton.classList.add("btn-info");
		sendButton.classList.remove("btn-secondary");
		sendButton.removeAttribute('disabled');
		sessionStorage.removeItem("remainTime");
	}, delayTime * 1000);
}


//提交功能实现
function submitFunc() {
	submitButton.addEventListener("click", () => {
		submitButton.setAttribute('disabled', 'disabled')
		$.ajax({
			url: '',
			type: 'POST',
			data: $('#register_form').serialize(),
			dataType: "JSON",
			success: (res) => {
				if (res.status === "success") {
					location.reload();
				} else {
					setTimeout(() => {
						submitButton.removeAttribute('disabled');
					}, 1000);
					for (let key in res.message) {
						console.log(key)
						document.querySelector(`#${key}_check`).innerText = res.message[key][0];
						setTimeout(() => {
							document.querySelector(`#${key}_check`).innerText = "";
						}, 2000)
					}
				}
			}
		})
	})
}


// 切换手机/邮箱注册
function switchMethod() {

	function regsiterWithPhone() {
		// 目前是手机注册状态，
		// 需要设置邮箱默认值并隐藏
		// 显示手机号与验证码，并清空
		// 按钮换成"邮箱注册"
		if (sessionStorage.getItem('username')) {
			usernameInput.value = sessionStorage.getItem('username');
		}
		if (sessionStorage.getItem('phone')) {
			phoneInput.value = sessionStorage.getItem('phone');
		}
		registerMethod = 'phone'
		sessionStorage.setItem("registerMethod", "phone")
		emailInput.value = "2333@x.com"
		emailInput.parentNode.classList.add("d-none")
		phoneInput.value = sessionStorage.getItem('phone') || ""
		codeInput.value = ""
		phoneInput.parentNode.classList.remove("d-none")
		codeBox.parentNode.classList.remove("d-none")
		registerMethodButton.value = "邮箱注册"
		if (sessionStorage.getItem('remainTime')) {
			startTimer();
		}
	}

	function registerWithEmail() {
		// 目前是邮箱注册状态，
		// 需要设置手机号、验证码默认值并隐藏
		// 显示邮箱，并清空
		// 按钮换成"手机注册"
		if (sessionStorage.getItem('username')) {
			usernameInput.value = sessionStorage.getItem('username');
		}
		if (sessionStorage.getItem('email')) {
			emailInput.value = sessionStorage.getItem('email');
		}
		registerMethod = 'email'
		sessionStorage.setItem("registerMethod", "email")
		phoneInput.value = "19800000000"
		codeInput.value = "100000"
		phoneInput.parentNode.classList.add("d-none")
		codeBox.parentNode.classList.add("d-none")
		emailInput.value = sessionStorage.getItem('email') || ""
		emailInput.parentNode.classList.remove("d-none")
		registerMethodButton.value = "手机注册"
	}

	if (!sessionStorage.getItem('registerMethod')) {
		// 初始化为邮箱登录
		registerWithEmail();
	} else {
		if (sessionStorage.getItem('registerMethod') === 'phone') {
			regsiterWithPhone()
		} else if (sessionStorage.getItem('registerMethod') === 'email') {
			registerWithEmail()
		} else {
			//pass
		}
	}

	//切换手机号/邮箱注册
	registerMethodButton.addEventListener("click", (e) => {
		if (e.target.value === "手机注册") {
			regsiterWithPhone()
		} else if (e.target.value === "邮箱注册") {
			registerWithEmail()
		} else {
			// pass
		}
	})
}

// 发送短信验证码 
function sendSms() {
	sendButton.addEventListener("click", (e) => {
		$.ajax({
			url: sendSmsUrl,
			data: {
				"phone": phoneInput.value,
				"csrfmiddlewaretoken": csrfToken,
				"tpl": "register",
			},
			type: "POST",
			dataType: "json",
			success: (res) => {
				if (res.status === 'success') {
					document.querySelector('#phone_check').innerText = "";
					startTimer();
				} else {
					document.querySelector('#phone_check').innerText = res.message;
					setTimeout(() => {
						document.querySelector('#phone_check').innerText = "";
					}, 2000)
				}
			},
		});
	})
}

// 保存注册数据到sessionStorage
function storageData() {
	setTimeout(() => {
		setInterval(() => {
			sessionStorage.setItem("username", usernameInput.value)
			if (registerMethod === 'phone') {
				sessionStorage.setItem("phone", phoneInput.value)
			} else {
				sessionStorage.setItem("email", emailInput.value)
			}
		}, 1000)
	}, 3000)
}


let registerMethod;
submitFunc();
switchMethod();
sendSms();
storageData();