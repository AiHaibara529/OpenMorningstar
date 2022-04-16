function checkCashRegister(price, cash, cid) {
	const Denomination = {
		"PENNY": 0.01,
		"NICKEL": 0.05,
		"DIME": 0.1,
		"QUARTER": 0.25,
		"ONE": 1,
		"FIVE": 5,
		"TEN": 10,
		"TWENTY": 20,
		"ONE HUNDRED": 100
	}
	const remain = cash - price;
	function get_sum(cid) {
		let sum = 0;
		for (let i = 0; i < cid.length; i++) {
			sum += cid[i][1]
		}
		return Math.round(sum * 100) / 100;
	}
	if (cash - price > get_sum(cid)) {
		return { status: "INSUFFICIENT_FUNDS", change: [] }
	} else if (cash - price == get_sum(cid)) {
		return { status: "CLOSED", change: cid }
	} else {
		let remain = cash - price;
		let newCid = [...cid];
		newCid.reverse();

		let change = newCid.map((item) => {
			let current_value = Denomination[item[0]];
			let current_change;
			let cashStorage = item[1];
			let change_need = parseInt(remain / current_value) * current_value;

			console.log(`当前面额：${current_value}, 剩余金额：${remain},收银柜余额：${cashStorage}`)
			if (remain < current_value) {
				current_change = 0;
			} else {
				if (change_need < item[1]) { //  本轮需要的数额 < 柜台剩余金额
					current_change = change_need;
				} else {
					current_change = cashStorage
				}
			}
			remain -= current_change
			remain = Math.round(remain * 100) / 100;
			console.log([item[0], current_change])
			return [item[0], current_change]
		})
		console.log(`最终剩余：${remain}`)
		if (remain > 0) {
			return { status: "INSUFFICIENT_FUNDS", change: [] }
		}
		change = change.filter(item => item[1] > 0);
		return { status: "OPEN", "change": change }
	}

}

checkCashRegister(3.26, 100, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]])
// checkCashRegister(3.26, 100, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]])
// checkCashRegister(19.5, 20, [["PENNY", 0.01], ["NICKEL", 0], ["DIME", 0], ["QUARTER", 0], ["ONE", 1], ["FIVE", 0], ["TEN", 0], ["TWENTY", 0], ["ONE HUNDRED", 0]])
// checkCashRegister(19.5, 20, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]])
