from flask import Flask , jsonify , request,send_file ,render_template
import pixellib
from pixellib.tune_bg import alter_bg
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)
picFolder = os.path.join('uploads','piclab')
app.config['UPLOAD_FOLDER'] = picFolder

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/" , methods=['POST' , 'GET'])
def backgroundchange():
    if request.method == "POST":
        if 'files[]' not in request.files:
            return jsonify({'msg':'File not selected'})
        else:
            files = request.files.getlist('files[]')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.abspath('uploads') +'/'+ filename)

            change_bg = alter_bg()
            change_bg.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
            output = change_bg.change_bg_img(f_image_path = 'uploads/'+files[0].filename  ,b_image_path = 'uploads/'+files[1].filename )
            cv2.imwrite("uploads/piclab/updatedimg.jpg", output)
            resImg = cv2.imread('uploads/piclab/updatedimg.jpg')
            os.unlink('uploads/'+files[0].filename)
            os.unlink('uploads/'+files[1].filename)
            return jsonify({"msg":"Successfully Uploaded!!"})  
   
    else:
    #    pic1 = cv2.imread('uploads/piclab/updatedimg.jpg')
    #    cv2.imshow('image', pic1) 
    #    cv2.waitKey(0)        
    #    cv2.destroyAllWindows()
       return jsonify({'msg':'successfully shown Image'})



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)    