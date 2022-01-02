from flask import Flask,jsonify,request,render_template,redirect,flash
from flask_restful import Resource,Api,reqparse
import PyPDF2
import os

app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = 'pdf'

path = os.getcwd()
print(os.getcwd())
if not(os.path.isdir(path+'/Converted')):
	os.mkdir(path+'/Converted')
	



def check(pdf,angle,pagenum):
	if pdf.filename == '':
		return {"Message" :"File has not been uploaded...",'status_code' : 301}

	if not ('.' in pdf.filename and pdf.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS) :
		return {"Message" :"Invalid file type...",'status_code' : 302}

	if(pagenum > PyPDF2.PdfFileReader(pdf,strict=False).numPages):
		return {"Message" :"Invalid page number(page number entered is greater than the total number of pages)...",'status_code' : 303}

	return {"Message" :"Page successfully rotated..",'status_code' : 200}


class Rotate(Resource):
	def post(self):
		
		pdf = request.files['pdf']
		angle=int(request.form['degree'])
		pagenum=int(request.form['pagenum'])

		resp=check(pdf,angle,pagenum)

		if(resp['status_code'] != 200):
			return jsonify(resp)

		pdf_reader = PyPDF2.PdfFileReader(pdf,strict=False)
		pdf_writer = PyPDF2.PdfFileWriter()
		totalpages= pdf_reader.numPages
		

		for pageno in range(totalpages):
			page = pdf_reader.getPage(pageno)
			if  pageno+1 == pagenum:
				page.rotateClockwise(angle)
			pdf_writer.addPage(page)
		
		pdf_out = open(os.path.join(path+'/Converted','Converted_'+str(angle)+'_'+pdf.filename), 'wb')
		pdf_writer.write(pdf_out)
		pdf_out.close()
		#print(pdf)
		return jsonify(resp)
			


#Home Page
@app.route('/', methods=['GET'])

def upload():
	return render_template("upload.html")



api.add_resource(Rotate,"/Rotate")

if __name__ == "__main__":
	app.run(debug=True)