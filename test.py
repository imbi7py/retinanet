import torch
import torchvision.transforms as transforms

from torch.autograd import Variable

from model.retina_shuffle import RetinaNet_Shuffle
from data_utils.encoder import DataEncoder
from PIL import Image, ImageDraw


print('Loading model..')
net = RetinaNet_Shuffle(20)
net.load_state_dict(torch.load('./checkpoint/ckpt.pth')['net'])
net.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

print('Loading image..')
img = Image.open(r'E:\md\IMG_20180317_172421R.jpg')
w = h = 300
img = img.resize((w, h))

print('Predicting..')
x = transform(img)
x = x.unsqueeze(0)
x = Variable(x, volatile=True)
loc_preds, cls_preds = net(x)

print('Decoding..')
encoder = DataEncoder()
boxes, labels = encoder.decode(loc_preds.data.squeeze(), cls_preds, (w, h))

draw = ImageDraw.Draw(img)
for box in boxes:
    draw.rectangle(list(box), outline='red')
img.show()