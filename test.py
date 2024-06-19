import tkinter as tk
root = tk.Tk()
root.title("SET Stock Trading Bot")
root.geometry("640x480")  # กำหนดขนาดหน้าต่างหลัก

main_frame = tk.Frame(root)
option_frame = tk.Frame(root, bg='light green')
option_frame.pack(side=tk.LEFT)
option_frame.pack_propagate(False)
option_frame.configure(width=160, height=640)

main_frame = tk.Frame(root)

main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=480, height=640)


def header():
    # สร้างเฟรมสำหรับภาพแบนเนอร์และ Label
    placecopricegraph_frame = tk.Frame(main_frame)
    placecopricegraph_frame.pack(pady=20)

    # Creating a photoimage object to use image
    image = tk.PhotoImage(file=r"./images/large_test_image.png")
    resized_banner_image = image.subsample(int(image.width()/480))

    # Display it within a label.
    pic = tk.Label(placecopricegraph_frame, image=resized_banner_image)
    pic.pack()

    # เพิ่ม Label "Price Checkr"
    label = tk.Label(placecopricegraph_frame,
                     text="Price Checkr", font=("Helvetica", 16, "bold"))
    label.pack()
    placecopricegraph_frame.pack(pady=20)

    # เก็บ reference ของภาพไว้ที่ label หรือ frame เพื่อป้องกันการถูกเก็บข้อมูลที่ไม่ใช้แล้ว
    pic.image = resized_banner_image


header()
# แสดงหน้าต่างหลัก
root.mainloop()
