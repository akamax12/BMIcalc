import json
import os


INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

import json
import os


def load_orders():

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)


            orders = data if isinstance(data, list) else [data] if isinstance(data, dict) else []


            valid_orders = []
            for order in orders:
                if not isinstance(order, dict):
                    continue


                order.setdefault('order_id', f"ORD{len(valid_orders)+1:03d}")
                order.setdefault('customer', '未知客户')
                order.setdefault('items', [])
                order.setdefault('status', '待處理')


                valid_items = []
                for item in order['items']:
                    if isinstance(item, dict):
                        item.setdefault('name', '未命名商品')
                        item.setdefault('price', 0)
                        item.setdefault('quantity', 1)
                        valid_items.append(item)

                order['items'] = valid_items
                valid_orders.append(order)

            return valid_orders

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("=> 警告：訂單文件不是JSON格式，將初始化空列表")
        return []
def save_orders(orders_list, filename=INPUT_FILE):

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(orders_list, f, indent=4, ensure_ascii=False)

def show_menu():
    print("***************選單***************")
    print("1. 新增訂單")
    print("2. 顯示訂單報表")
    print("3. 出餐處理")
    print("4. 離開")
    print("**********************************")

def add_order():
    print("請輸入訂單編號：", end="")
    order_id = input().strip()
    print("請輸入顧客姓名：", end="")
    customer_name = input().strip()

    items = []
    while True:
        print("請輸入訂單項目名稱（輸入空白結束）：", end="")
        item_name = input().strip()
        if not item_name:
            break

        print("請輸入價格：", end="")
        try:
            price = int(input())
        except ValueError:
            print("價格必須是數字，請重新輸入！")
            continue

        print("請輸入數量：", end="")
        try:
            quantity = int(input())
        except ValueError:
            print("數量必須是數字，請重新輸入！")
            continue

        items.append({
            'name': item_name,
            'price': price,
            'quantity': quantity
        })

    if not items:
        print("=> 訂單未新增，因為沒有項目！")
        return

    orders.append({
        'order_id': order_id.upper(),
        'customer': customer_name,
        'items': items,
        'status': '待處理'
    })

    save_orders(orders)
    print(f"=> 訂單 {order_id.upper()} 已新增！")

def show_report():
    if not orders:
        print("=> 目前沒有任何訂單！")
        return

    print("\n==================== 訂單報表 ====================")
    for i, order in enumerate(orders, 1):

        order_id = order.get('order_id', f'未知編號_{i}')
        customer = order.get('customer', '未知客戶')
        items = order.get('items', [])
        status = order.get('status', '狀態未知')

        print(f"\n訂單 #{i}")
        print(f"訂單編號: {order_id}")
        print(f"客户名稱: {customer}")
        print("--------------------------------------------------")
        print("商品名稱\t單價\t數量\t總計")
        print("--------------------------------------------------")

        total = 0
        for item in items:
            name = item.get('name', '未命名商品')
            price = item.get('price', 0)
            quantity = item.get('quantity', 1)
            subtotal = price * quantity
            print(f"{name}\t{price}\t{quantity}\t{subtotal}")
            total += subtotal

        print("--------------------------------------------------")
        print(f"訂單總額: {total}")
        print(f"狀態: {status}")
    print("==================================================\n")

def process_order():
    global orders
    if not orders:
        print("=> 目前沒有任何訂單！")
        return


    pending_orders = []
    for order in orders:
        if isinstance(order, dict):
            status = order.get('status', '待處理')  
            if status == '待處理':
                pending_orders.append(order)
        else:
            print(f"=> 警告：忽略訂單數據: {order}")

    if not pending_orders:
        print("=> 目前没有待處理訂單！")
        return

        print("\n======== 待處理列表 ========")
    for i, order in enumerate(pending_orders, 1):
        print(f"{i}. 訂單編號: {order.get('order_id', '未知')} - 客户: {order.get('customer', '未知')}")
        print("================================")

    while True:
        print("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ", end="")
        choice = input().strip()

        if not choice:
            return

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(pending_orders):
                selected_order = pending_orders[choice_num - 1]
                selected_order['status'] = '已出餐'


                save_orders(orders)


                output_orders = [order for order in orders if order['status'] == '已出餐']
                save_orders(output_orders, OUTPUT_FILE)

                print(f"=> 訂單 {selected_order['order_id']} 已出餐完成")
                print("出餐訂單詳細資料：\n")

                print("==================== 出餐訂單 ====================")
                print(f"訂單編號: {selected_order['order_id']}")
                print(f"客戶姓名: {selected_order['customer']}")
                print("--------------------------------------------------")
                print("商品名稱\t單價\t數量\t總計")
                print("--------------------------------------------------")

                total = 0
                for item in selected_order['items']:
                    subtotal = item['price'] * item['quantity']
                    print(f"{item['name']}\t{item['price']}\t{item['quantity']}\t{subtotal}")
                    total += subtotal

                print("--------------------------------------------------")
                print(f"訂單總額: {total}")
                print("==================================================")
                break
            else:
                print(f"=> 錯誤：請輸入有效的數字範圍 (1-{len(pending_orders)})")
        except ValueError:
            print("=> 錯誤：請輸入有效的數字")

def main():
    global orders
    orders = load_orders()


    if not isinstance(orders, list):
        orders = []



    while True:
        show_menu()
        print("請選擇操作項目(Enter 離開)：", end="")
        choice = input().strip()

        if not choice or choice == '4':
            print("=> 感謝使用訂單管理系統！")
            break

        if choice == '1':
            add_order()
        elif choice == '2':
            show_report()
        elif choice == '3':
            process_order()
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()