from scheule import *

akb = Akb("2018/10/20")
ske = Ske("2018/10/20")

akb_scheule = akb.get_scheule()

print(akb_scheule.__len__())