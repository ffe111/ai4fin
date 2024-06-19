import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from settrade_v2 import *
import csv
from investing import *
from sentiment import *
from scrap import *


def test():
    return


root = tk.Tk()
root.title("SET Stock Trading Bot")
root.geometry("640x480")  # กำหนดขนาดหน้าต่างหลัก

option_frame = tk.Frame(root, bg='light green')


def get_accinfo(master):
    import csv
    import tkinter as tk
    from tkinter import messagebox

    # Assuming Investor and other necessary imports are defined elsewhere in your script
    with open('user_info.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            app_id = row['App Id']
            app_secret = row['App Secret']
            broker_id = row['Broker Id']
            app_code = row['App Code']
            acc_no = row['Account no']

    investor = Investor(
        app_id=app_id,
        app_secret=app_secret,
        broker_id=broker_id,
        app_code=app_code,
        is_auto_queue=False
    )
    equity = investor.Equity(account_no=acc_no)
    try:
        # Changed from get_orders to get_account_info
        portfolio = equity.get_account_info()

        if portfolio:  # Assuming 'portfolio' contains the account information
            new_window = tk.Toplevel(master)
            new_window.title("Account Information")
            new_window.geometry("360x260")

            default_font = ("Arial", 12)
            text_widget = tk.Text(new_window, wrap="word",
                                  padx=10, pady=10, font=default_font)
            text_widget.pack(expand=True, fill="both")

            # Assuming portfolio is a dictionary containing account information
            # You will need to adjust the keys according to your actual data structure
            for key, value in portfolio.items():
                formatted_info = f"{key}: {value}\n"
                text_widget.insert("end", formatted_info)

            text_widget.config(state="disabled")
        else:
            messagebox.showinfo("No Account Info",
                                "No account information found.")

    except Exception as e:
        messagebox.showerror(
            "Error", f"Error getting account information: {e}")


def user_management_page():
    user_management_frame = tk.Frame(main_frame)

    # lb = tk.Label(user_management_frame,
    #               text="Home Page\n\nPage 1", font=('Bold', 20))
    # lb.pack()
    user_management_frame.pack(pady=20)

    # label = tk.Label(user_management_frame, text="User Management",
    #                  font=("Helvetica", 16, "bold"))
    # label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")
    header_grid(user_management_frame, text="User Management",
                nimage="user_mange_pic")
    # โหลดข้อมูลจากไฟล์ CSV ถ้ามี
    user_info = load_user_info()

    # สร้างช่องใส่ข้อมูล
    app_id_label = tk.Label(user_management_frame, text="App Id:")
    app_id_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    app_id_entry = tk.Entry(user_management_frame)
    app_id_entry.grid(row=2, column=1, padx=10, pady=5)
    if user_info:
        app_id_entry.insert(0, user_info[0])

    app_secret_label = tk.Label(user_management_frame, text="App Secret:")
    app_secret_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    app_secret_entry = tk.Entry(user_management_frame)
    app_secret_entry.grid(row=3, column=1, padx=10, pady=5)
    if user_info:
        app_secret_entry.insert(0, user_info[1])

    broker_id_label = tk.Label(user_management_frame, text="Broker Id:")
    broker_id_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
    broker_id_entry = tk.Entry(user_management_frame)
    broker_id_entry.grid(row=4, column=1, padx=10, pady=5)
    if user_info:
        broker_id_entry.insert(0, user_info[2])

    app_code_label = tk.Label(user_management_frame, text="App Code:")
    app_code_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
    app_code_entry = tk.Entry(user_management_frame)
    app_code_entry.grid(row=5, column=1, padx=10, pady=5)
    if user_info:
        app_code_entry.insert(0, user_info[3])

    account_no_label = tk.Label(user_management_frame, text="Account no:")
    account_no_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
    account_no_entry = tk.Entry(user_management_frame)
    account_no_entry.grid(row=6, column=1, padx=10, pady=5)
    if user_info:
        account_no_entry.insert(0, user_info[4])

    # สร้างปุ่มสำหรับการยืนยันการทำรายการ
    confirm_button = tk.Button(user_management_frame, text="Confirm", command=lambda: submit_user_info(app_id_entry.get(
    ), app_secret_entry.get(), broker_id_entry.get(), app_code_entry.get(), account_no_entry.get()))
    confirm_button.grid(row=7, column=0, columnspan=2, pady=10)

    port_button = tk.Button(user_management_frame, text="UserInfo",
                            command=lambda: get_accinfo(user_management_frame))
    port_button.grid(row=7, column=1, columnspan=2, pady=10)


def submit_user_info(app_id, app_secret, broker_id, app_code, account_no):
    # ฟังก์ชันสำหรับการยืนยันข้อมูลผู้ใช้
    print("App Id:", app_id)
    print("App Secret:", app_secret)
    print("Broker Id:", broker_id)
    print("App Code:", app_code)
    print("Account no:", account_no)

    # เซฟข้อมูลลงในไฟล์ CSV
    with open('user_info.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['App Id', 'App Secret', 'Broker Id',
                        'App Code', 'Account no'])
        writer.writerow([app_id, app_secret, broker_id, app_code, account_no])

    # แสดงข้อความแจ้งเตือน
    messagebox.showinfo("Success", "User info has been saved.")


def load_user_info():
    try:
        with open('user_info.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # ข้ามหัวข้อ
            return next(reader, [])  # อ่านข้อมูลหากมี หากไม่มีให้คืนค่าว่าง
    except FileNotFoundError:
        return []


def header(frame, text, nimage):
    # Creating a photoimage object to use image
    # แทนที่ "banner_image.png" ด้วยตำแหน่งและชื่อไฟล์ของภาพแบนเนอร์ของคุณ
    banner_image = tk.PhotoImage(file=f"./images/{nimage}.png")
    resized_banner_image = banner_image.subsample(
        int(banner_image.width()/480))
    banner_label = tk.Label(frame,
                            image=resized_banner_image)
    banner_label.pack()

    # เพิ่ม Label "Price Checkr"
    label = tk.Label(frame,
                     text=text, font=("Helvetica", 16, "bold"))
    label.pack()
    frame.pack(pady=20)
    banner_label.image = resized_banner_image


def pricegraph_page():
    # สร้างเฟรมสำหรับภาพแบนเนอร์และ Label
    placecopricegraph_frame = tk.Frame(main_frame)
    placecopricegraph_frame.pack(pady=20)

    header(placecopricegraph_frame, text="Price Checkr", nimage="check_price_pic")
    # Create input field
    entry_label = tk.Label(placecopricegraph_frame, text="Enter Stock ID:")
    entry_label.pack(pady=10)
    global entry
    entry = tk.Entry(placecopricegraph_frame)
    entry.pack()

    # Create button to fetch price
    fetch_button = tk.Button(placecopricegraph_frame,
                             text="Check Price", command=get_stock_price)
    fetch_button.pack(pady=10)

    # Create label to display result
    global result_label
    result_label = tk.Label(placecopricegraph_frame, text="")
    result_label.pack()


def get_stock_price():
    # Get stock ID from entry field
    stock_id = entry.get()

    # Retrieve stock price information
    price_data = stock_price(stock_id)
    if price_data:
        # Create a new window to display the stock price information
        # สมมติว่า 'root' คือหน้าต่างหลักของแอปพลิเคชัน Tkinter
        new_window = tk.Toplevel(root)
        new_window.title(f"Stock Price Information for {stock_id}")

        # Create a label in the new window for displaying the information
        info_label = tk.Label(new_window, text="",
                              justify=tk.LEFT, padx=10, pady=10)
        info_label.pack()

        # Update the label with price information
        info_label.config(text=f"Symbol : {price_data['symbol']}\n"
                          f"Name : {price_data['nameEN']}\n"
                          f"Price : {price_data['offers']}\n"
                          f"High : {price_data['high']}\n"
                          f"Low : {price_data['low']}\n"
                          f"Average : {price_data['average']}\n"
                          f"Change : {price_data['percentChange']}\n"
                          f"Market Status : {price_data['marketStatus']}\n"
                          f"Last update : {price_data['marketDateTime']}")
    else:
        messagebox.showinfo("No Symbol", "No Symbol found.")


def header_grid(frame, text, nimage):
    banner_image = tk.PhotoImage(file=f"./images/{nimage}.png")
    resized_banner_image = banner_image.subsample(
        int(banner_image.width()/480))
    banner_label = tk.Label(frame, image=resized_banner_image)
    banner_label.grid(row=0, column=0, columnspan=2, pady=10)

    label = tk.Label(frame, text=text,
                     font=("Helvetica", 16, "bold"))
    label.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")
    frame.pack(pady=20)
    banner_label.image = resized_banner_image


def placecommand_page():
    placecommand_frame = tk.Frame(main_frame)

    header_grid(placecommand_frame, text="Place Order",
                nimage="place_order_pic")

    # สร้างช่องใส่ข้อมูล
    stock_name_label = tk.Label(placecommand_frame, text="Stock Name:")
    stock_name_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    stock_name_entry = tk.Entry(placecommand_frame)
    stock_name_entry.grid(row=2, column=1, padx=10, pady=5)

    price_label = tk.Label(placecommand_frame, text="Price:")
    price_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    price_entry = tk.Entry(placecommand_frame)
    price_entry.grid(row=3, column=1, padx=10, pady=5)

    quantity_label = tk.Label(placecommand_frame, text="Quantity:")
    quantity_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
    quantity_entry = tk.Entry(placecommand_frame)
    quantity_entry.grid(row=4, column=1, padx=10, pady=5)

    transaction_type_label = tk.Label(
        placecommand_frame, text="Transaction Type:")
    transaction_type_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
    transaction_type_var = tk.StringVar()
    transaction_type_var.set("Buy")
    transaction_type_menu = tk.OptionMenu(
        placecommand_frame, transaction_type_var, "Buy", "Sell")
    transaction_type_menu.grid(row=5, column=1, padx=10, pady=5)

    # สร้างปุ่มสำหรับการยืนยันการทำรายการ
    confirm_button = tk.Button(placecommand_frame, text="Confirm", command=lambda: submit_transaction(stock_name_entry.get(
    ), price_entry.get(), quantity_entry.get(), transaction_type_var.get()))
    confirm_button.grid(row=6, column=0, columnspan=2, pady=10)


def submit_transaction(stock_name_entry, price_entry, quantity_entry, transaction_type_var):

    stock_name = stock_name_entry  # Remove leading/trailing whitespace

    # Validate user input
    if not stock_name:
        messagebox.showerror("Error", "Please enter a stock name.")
        return

    try:
        price = float(price_entry)
    except ValueError:
        messagebox.showerror("Error", "Price must be a number.")
        return

    if price <= 0:
        messagebox.showerror("Error", "Price must be greater than 0.")
        return

    try:
        quantity = int(quantity_entry)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    if quantity <= 0:
        messagebox.showerror("Error", "Quantity must be greater than 0.")
        return
    # Confirmation dialog
    if messagebox.askquestion("Confirm Order", f"Are you sure you want to place this order?") != "yes":
        return  # User canceled confirmation
    # Connect to the API
    import csv

    with open('user_info.csv', mode='r') as file:

        csv_reader = csv.DictReader(file)
        # วนลูปผ่านแต่ละแถวในไฟล์ CSV
        for row in csv_reader:
            # นี่คือตัวอย่างการเรียกใช้งานตัวแปรในไฟล์ CSV
            app_id = row['App Id']
            app_secret = row['App Secret']
            broker_id = row['Broker Id']
            app_code = row['App Code']
            acc_no = row['Account no']

    investor = Investor(
        app_id=app_id,
        app_secret=app_secret,
        broker_id=broker_id,
        app_code=app_code,
        is_auto_queue=False
    )
    equity = investor.Equity(account_no=acc_no)

    # Place the order
    try:
        place_order = equity.place_order(
            pin="000000",
            symbol=stock_name,
            side=transaction_type_var,
            price=price,
            volume=quantity,
        )
        # รับ Order ID จากการสั่งซื้อ
        order_id = place_order.get('order_id', None)
        messagebox.showinfo(
            "Success", f"Order placed successfully! Order ID: {order_id}")
        # Print confirmation details only if successful
        print("Stock Name:", stock_name)
        print("Price:", price)
        print("Quantity:", quantity)
        print("Transaction Type:", transaction_type_var)
    except Exception as e:
        # Handle potential errors and check for market closure or order rejection
        error_message = f"Error placing order: {e}"
        # Check for specific error messages
        if "Market is closed" in str(e) or "Order rejected" in str(e):
            error_message = "Market is closed or order cannot be placed."
        messagebox.showerror("Error", error_message)


def check_order(master):
    import csv

    with open('user_info.csv', mode='r') as file:

        csv_reader = csv.DictReader(file)
        # วนลูปผ่านแต่ละแถวในไฟล์ CSV
        for row in csv_reader:
            # นี่คือตัวอย่างการเรียกใช้งานตัวแปรในไฟล์ CSV
            app_id = row['App Id']
            app_secret = row['App Secret']
            broker_id = row['Broker Id']
            app_code = row['App Code']
            acc_no = row['Account no']

    investor = Investor(
        app_id=app_id,
        app_secret=app_secret,
        broker_id=broker_id,
        app_code=app_code,
        is_auto_queue=False
    )
    equity = investor.Equity(account_no=acc_no)
    orders = equity.get_orders()
    # For loop to print the desired information from each order in the format specified by the user
    # for order in orders:
    #     print(f"{order['orderNo']}: {order['accountNo']} {order['symbol']} {order['tradeTime']} {order['side']} {order['priceType']} {order['price']}")

    # สร้างหน้าต่างใหม่
    if orders:  # สมมติว่า 'orders' เป็นตัวแปรที่มีรายการออเดอร์
        new_window = tk.Toplevel(master)
        new_window.title("Order List")
        new_window.geometry("360x260")

        default_font = ("Arial", 12)
        text_widget = tk.Text(new_window, wrap="word",
                              padx=10, pady=10, font=default_font)
        text_widget.pack(expand=True, fill="both")

        for order in orders:
            formatted_order_no = f"Order No: {order['orderNo']}\n"
            formatted_account_no = f"Account No: {order['accountNo']}\n"
            formatted_symbol = f"Symbol: {order['symbol']}\n"
            formatted_trade_time = f"Trade Time: {order['tradeTime']}\n"
            formatted_side = f"Side: {order['side']}\n"
            formatted_price = f"Price: {order['price']}\n"

            text_widget.insert("end", formatted_order_no, "order_no")
            text_widget.insert("end", formatted_account_no, "account_no")
            text_widget.insert("end", formatted_symbol, "symbol")
            text_widget.insert("end", formatted_trade_time, "trade_time")
            text_widget.insert("end", formatted_side, "side")
            text_widget.insert("end", formatted_price, "price")
            text_widget.insert("end", "-" * 50 + "\n")

        # กำหนดสไตล์สำหรับแต่ละส่วนของข้อมูลออเดอร์
        text_widget.tag_configure("order_no", font=("Arial", 12, "bold"))
        text_widget.tag_configure("account_no", foreground="#007acc")
        text_widget.tag_configure("symbol", foreground="#009900")
        # สามารถเพิ่ม tag_configure สำหรับส่วนอื่นๆ ตามต้องการ

        text_widget.config(state="disabled")
    else:
        messagebox.showinfo(
            "No Orders", "No orders found.")


def canclecommand_page():
    canclecommand_frame = tk.Frame(main_frame)

    # lb = tk.Label(canclecommand_frame,
    #               text="canclecommand_frame Page\n\nPage 4", font=('Bold', 20))
    # lb.pack()
    # canclecommand_frame.pack(pady=20)

    # label = tk.Label(canclecommand_frame, text="Cancle Order",
    #                  font=("Helvetica", 16, "bold"))
    # label.pack()

    header(canclecommand_frame, text="Cancel Order", nimage="cancel_order_pic")
    # สร้าง Label และ Entry widget สำหรับ ID คำสั่งซื้อ
    order_id_label = tk.Label(canclecommand_frame, text="Order ID:")
    order_id_label.pack(pady=10)
    order_id_entry = tk.Entry(canclecommand_frame)
    order_id_entry.pack(pady=10)

    # สร้างปุ่ม "Cancel"
    cancel_button = tk.Button(canclecommand_frame, text="Cancel", command=lambda: cancel_order(
        order_id_entry.get()))
    cancel_button.pack(pady=10)

    order_button = tk.Button(canclecommand_frame, text="Check Order",
                             command=lambda: check_order(canclecommand_frame))
    order_button.pack(pady=5)


def cancel_order(order_id):

    # Validate order ID input
    if not order_id:
        messagebox.showerror("Error", "Please fill the order ID field.")
        return

    # Connect to the API and cancel order
    import csv

    with open('user_info.csv', mode='r') as file:

        csv_reader = csv.DictReader(file)
        # วนลูปผ่านแต่ละแถวในไฟล์ CSV
        for row in csv_reader:
            # นี่คือตัวอย่างการเรียกใช้งานตัวแปรในไฟล์ CSV
            app_id = row['App Id']
            app_secret = row['App Secret']
            broker_id = row['Broker Id']
            app_code = row['App Code']
            acc_no = row['Account no']

    investor = Investor(
        app_id=app_id,
        app_secret=app_secret,
        broker_id=broker_id,
        app_code=app_code,
        is_auto_queue=False
    )
    equity = investor.Equity(account_no=acc_no)

    try:
        # Assuming cancel_order supports DELETE
        equity.cancel_order(order_id, pin='000000')
        messagebox.showinfo("Success", "Order has been cancelled.")
    except Exception as e:
        messagebox.showerror("Error", f"Error cancelling order: {e}")


def news_page():
    news_frame = tk.Frame(main_frame)

    # lb = tk.Label(news_frame,
    #               text="news_frame Page\n\nPage 5", font=('Bold', 20))
    # lb.pack()
    # news_frame.pack(pady=20)
    # label = tk.Label(news_frame, text="News Analyze",
    #                  font=("Helvetica", 16, "bold"))
    # label.pack()
    # news_frame.pack(pady=20)
    header(news_frame, text="News Analyze", nimage="analyze_news_pic")

    url = "https://www.investing.com/commodities/crude-oil-news"
    headlines = [{new: estimate_sentiment(new)}
                 for new in scraping(url) if new != None]
    # print(headlines)
    if headlines:
        default_font = ("Arial", 12)
        text_widget = tk.Text(news_frame, wrap="word",
                              padx=10, pady=10, font=default_font)
        text_widget.pack(expand=True, fill="both")
        # text_widget.insert("end", "News and Sentiment Analysis:\n\n")
        unique_headlines = list(headlines)
        for headline in unique_headlines:
            formatted_headline = f"Headline: {list(headline.keys())[0]}\n"
            formatted_sentiment = f"Sentiment: {list(headline.values())[0][1]}\n"
            formatted_score = f"Pred Score: {list(headline.values())[0][0]}\n"
            text_widget.insert("end", formatted_headline, "headline")
            text_widget.insert("end", formatted_sentiment, "sentiment")
            text_widget.insert("end", formatted_score, "pred")
            text_widget.insert("end", "-" * 50 + "\n")
        text_widget.tag_configure("headline", font=("Arial", 12, "bold"))
        text_widget.tag_configure("sentiment", foreground="#007acc")
        text_widget.tag_configure("pred", foreground="#009900")
        text_widget.config(state="disabled")
    else:
        messagebox.showinfo(
            "No Headlines", "No headlines found for gold news on this page.")


def hide_indicate():
    user_management_indicate.config(bg="light green")
    pricegraph_indicate.config(bg="light green")
    placecommand_indicate.config(bg="light green")
    canclecommand_indicate.config(bg="light green")
    news__indicate.config(bg="light green")
    exit__indicate.config(bg="light green")


def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()


def indicate(lb, page):
    hide_indicate()
    lb.config(bg="dark green")
    delete_pages()
    page()


user_management_button = tk.Button(
    option_frame, text="User Management", command=lambda: indicate(user_management_indicate, user_management_page), width=20, height=2, bd=0, bg="light green", fg="green", font=('Bold', 12))
user_management_button.place(relx=0.5, rely=0.45, anchor="center")
user_management_indicate = tk.Label(option_frame, text='', bg="light green")
user_management_indicate.place(x=3, rely=0.40, width=5, height=50)


pricegraph_button = tk.Button(
    option_frame, text="Check Price", command=lambda: indicate(pricegraph_indicate, pricegraph_page), width=20, height=2, bd=0, bg="light green", fg="green", font=('Bold', 12))
pricegraph_button.place(relx=0.5, rely=0.55, anchor="center")
pricegraph_indicate = tk.Label(option_frame, text='', bg="light green")
pricegraph_indicate.place(x=3, rely=0.50, width=5, height=50)


placecommand_button = tk.Button(
    option_frame, text="Place Command", command=lambda: indicate(placecommand_indicate, placecommand_page), width=20, height=2, bd=0, bg="light green", fg="green", font=('Bold', 12))
placecommand_button.place(relx=0.5, rely=0.65, anchor="center")
placecommand_indicate = tk.Label(option_frame, text='', bg="light green")
placecommand_indicate.place(x=3, rely=0.60, width=5, height=50)


canclecommand_button = tk.Button(
    option_frame, text="Cancel Command", command=lambda: indicate(canclecommand_indicate, canclecommand_page), width=20, height=2, bd=0, bg="light green", fg="green", font=('Bold', 12))
canclecommand_button.place(relx=0.5, rely=0.75, anchor="center")
canclecommand_indicate = tk.Label(option_frame, text='', bg="light green")
canclecommand_indicate.place(x=3, rely=0.70, width=5, height=50)


news_button = tk.Button(option_frame, text="Analyze News",
                        command=lambda: indicate(news__indicate, news_page), width=20, height=2, bd=0, bg="light green", fg="green", font=('Bold', 12))
news_button.place(relx=0.5, rely=0.85, anchor="center")
news__indicate = tk.Label(option_frame, text='', bg="light green")
news__indicate.place(x=3, rely=0.80, width=5, height=50)


def exit_program():
    root.destroy()


exit_button = tk.Button(option_frame, text="Exit",
                        command=exit_program, width=20, height=2, bd=0, bg="light green", fg="green", font=('Bold', 12))
exit_button.place(relx=0.5, rely=0.95, anchor="center")
exit__indicate = tk.Label(option_frame, text='', bg="light green")
exit__indicate.place(x=3, rely=0.90, width=5, height=50)


option_frame.pack(side=tk.LEFT)
option_frame.pack_propagate(False)
option_frame.configure(width=160, height=640)

main_frame = tk.Frame(root)

main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=480, height=640)

# โหลดรูปภาพ
# image = Image.open("arrow.png")
bg_image = tk.PhotoImage(file="Trading_bot_bg.png")

# Set background image
background_label = tk.Label(main_frame, image=bg_image)
background_label.place(relwidth=1, relheight=1)

root.mainloop()
