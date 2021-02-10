dict_business_intent = {}

dict_business_intent["duration"] = ["mấy năm","chừng nào","tới chừng nào","tới mấy năm","bao lâu","may nam","chung nao","học có lâu không","có lâu không","bốn năm","4 năm","5 năm","năm năm","bao nhiêu năm","bao lau","bao nhieu nam","bao nhiêu học kỳ","bao nhiêu học kì","mấy học kì","mấy học kỳ","may hoc ky","may hoc ki","có lâu","lâu"]

dict_business_intent["location"] = ["học ở đâu","học ở chỗ nào","học ở cs nào","học ở cơ sở nào","hoc o cho nao","hoc o cs nao","học ở cơ sở 1","học ở cở sở 2","học ở cs1","học ở cs2","học ở nước ngoài","nước nào","nuoc ngoai","nuoc nao","học ở mỹ","học ở nhật"]

dict_business_intent["public_transport"] = ["buýt","xe buýt","bus","xe buyt","buyt","tuyến xe","xe số","xe bus","xe số mấy","xe so may","bus so may","xe buýt nào","xe buyt nao","xe nao","xe nào","tuyến nào","tuyen nao","tuyến số mấy","số mấy","tuyen so may","so may","trạm xe buýt","trạm xe số mấy","tram bus","trạm bus","trạm nào","trạm dừng","trạm","tram"]

dict_business_intent["accommodation"] = ["chỗ ở","ở chỗ nào","có chỗ ở","ktx","ký túc xá","kí túc xá","ky tuc xa","ki tuc xa","nên ở đâu","ở đâu","chỗ ăn chỗ ở","cho an cho o","nhà trọ","nha tro","nhà ở","nha o","cho o","cho an","ở trọ","o tro","nhà trọ","phòng trọ","phong tro","chung cu","chung cư","thuê phòng","thuê nhà","nha tro"]

dict_business_intent["address"] = ["địa chỉ","cơ sở 2 ở đâu","cơ sở 1 ở đâu","cs2","cs1","cs2 ở đâu","cs1 ở đâu","địa chỉ cs2","địa chỉ cs1","địa chỉ của trường","dia chi","dia chi cs2","dia chi cs1","ben tre","bến tre"]

dict_business_intent["out_come"] = ["yêu cầu đầu ra","chuẩn đầu ra","đầu ra","dau ra","yeu cau dau ra","chuan dau ra","chuẩn ra trường","chuẩn tốt nghiệp","yêu cầu tốt nghiệp","chuan tot nghiep","chuan ra truong","chuẩn tiếng anh","chuan tieng anh","chuẩn ngoại ngữ","chuan ngoai ngu","yêu cầu tiếng anh","yêu cầu ngoại ngữ","yeu cau ngoai ngu"]

dict_business_intent["subject_group"] = ["khối nào","thi khối nào","khoi nao","khoi nào","khói nào","khối nao","khói nao","có khối nào","co khoi nao","những khối nào","gồm khối nào","gom khoi nao"]

dict_business_intent["tuition"] = ["học phí","hoc phí","học phi","hoc phi","mắc","có mắc","rẻ","có rẻ","đắt","có đắt","đắc","có đắc","học phí là bao nhiêu","học phí bao nhiêu","tiền học","tiền","tien hoc","giá","giá tín chỉ","giá tiền","gia tien","giá tiền của"]

dict_business_intent["point"] = ["điểm","điểm chuẩn","điểm sàn","nhiêu điểm","bao nhiêu điểm","mấy điểm","điểm thi năm","điểm bao nhiêu","diem thi","bao nhiêu điểm","diem san","điểm thi bao nhiêu","điểm đạt không","điểm tốt không","điểm thấp không","thi nhiêu điểm","điểm nhiêu","mấy điểm","được nhiêu","điểm thi năm","công bố điểm thi","điểm nhiêu","mấy điểm","điểm bao nhiêu","nhieu diem","được nhiêu điểm","mấy điểm","điểm bao nhiêu","bao nhiêu điểm","có nhiêu điểm","điểm thi","mấy điểm","đậu hông","may diem","điểm bao nhiêu","bao nhieu diem","kết quả thi","điểm thi","điểm xét tuyển","diem","bao nhieu diem","điểm bao nhiêu","nhiêu điểm","mấy điểm","bao nhiu diem","diem bao nhiu","may diem","nhiêu điểm","được nhiêu","điểm thi bao nhiêu","điểm mấy","thi nhiêu điểm","bao nhiêu điểm","mấy điểm","điểm thế nào","điểm sao rồi","điểm ổn không","điểm nhiêu","điểm thế nào","bao nhiêu điểm","bao nhieu điểm","điểm chuẩn","điểm","diem chuan đh","mấy điểm đậu","bao nhiều điểm","bao nhiêu điểm","điểm","mấy điểm","điểm bao nhiêu","bao nhiêu điểm","điểm là","diem chuan"]

dict_business_intent["major_code"] = ["mã ngành","mã ngành bao nhiêu","mã ngành là gì","mã ngành","mã của ngành","mã bao nhiêu","mã ngành","mã mấy","ma nganh la","mã của ngành","mã ngành này","mã ngành","mã bao nhiêu","mã là","mã nhiêu","mã ngành nào","mã của ngành là nhiêu","mã ngành","mã ngành là gì","mã ngành","mã ngành bao nhiêu","mã ngành","mã của ngành","mã là gì","mã ngành","mã nganh","ma ngành","mã gì","mã về ngành","mã mấy","mã ngành học","ma ngành","ma đăng kí","ma ngành","ma ngành","mã ngành","mã ngành bao nhiêu","mã nào","mã của ngành","ma nganh bao nhiu","ma nganh nao","ma nganh","mã ngành nào","mã bao nhiêu","mã là gì","ma may vay","mã ngành nào","mã ngành học","mã của ngành","mã ngành","ngành này","mã xét tuyển","ma nganh","mã của ngành","mã là gì","mã bao nhiêu vậy","ma nganh"]

dict_business_intent["subject"] = ["môn thi","mon thi","môn nào","mon nao","tổ hợp","tổ hợp môn","môn"]

dict_random_intent = {}

dict_random_intent["anything"] = ["không phải","khong phai","sai","nào cũng được","bất kỳ","bất kì","bất kể","sao cũng được","sao cung duoc","anything","gì cũng được","nào cũng được","không biết","j cung dc","nao cung dc","sao cung dc","nào cũng được","cũng được","cung dc","cung duoc","sao cũng đc"]

dict_random_intent["hello"] = ["chào"," xin chào","chao","xin chao","hello","chao buoi sang","chào buổi sáng","hi "]
dict_random_intent["done"] = ["tạm biệt","bye bye","pp","tam biet","bye"]
dict_random_intent["thanks"] = ["đúng","phải rồi","ok","ừ","ừm","oke","yes","hay quá","cảm ơn","cam on","tks","thanks","thank","thank u","thank you","cám ơn","ty","đúng rồi","tốt lắm","cảm ơn nha","vang","vâng","đúng vậy","chính xác"]


