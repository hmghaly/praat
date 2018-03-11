import os, re, json
from itertools import groupby
from sys import argv

def textgrid_2_dict(fpath,order_elements=False): #process the contents of textgrid file and return as a dictinoary 
	#parameters: fpath = file path, order_elements = if we want elements (points and intervals) presented as an ordered list within each tier or as an unordered dictionary
	open_item="" #identify which item/tier are we currently working with
	open_element="" #identify which element (point/interval) are we currently working with
	#order_elements=False #if we want elements (points and intervals) presented as an ordered list within each tier or as an unordered dictionary
	final_list=[]
	fopen=open(fpath)
	for fi,f in enumerate(fopen): #iterating over the entire textgrid file, line by line
		cur_line=f.strip("\t\n\r ") #strip the whitespaces and line breaks
		if not cur_line: continue #skip empty lines
		if cur_line=='item []:': continue #skip the empty item line 
		if cur_line.lower().startswith("item") and cur_line[-1]==":" : open_item,open_element=cur_line, "" #for non-empty items, indicate it as the current active item, and indicate that there is no active/open element
		elif cur_line[-1]==":" : open_element=cur_line #otherwise if the current line ends with colon, indicate that it is an active/open element
		if cur_line[-1]==":": continue #now we want to move to the contents of the elements, so we skip processing the lines that end with colon
		split=[v.strip() for v in cur_line.split("=")] #we split each item around equal sign
		if len(split)==2: #if we have 2 split strings, we process them as key and value 
			key,val = split
			#print "????", val
			if val.startswith('"'): #this is a string value
				our_val=val.strip('"')
			else: #this is a numerical value
				try: our_val=int(val.strip('"')) #check if int
				except:
					try: our_val=float(val.strip('"')) #check if float
					except: our_val=val.strip('"') #else, treat it as string
			#print key, our_val
			final_list.append((open_item, open_element,key, our_val)) #put all keys, values, together with their active items (tiers) and elements into a list


	fopen.close()
	grouped=[(key,[v[1:] for v in list(group)]) for key,group in groupby(final_list,lambda x:x[0])] #we group the list by the items
	final_dict={}
	for k, grp in grouped:
		if k=="": #for the first information lines about the file, outside the items
			for g in grp:
				final_dict[g[-2]]=g[-1] #put these keys and values directly into our output dictionary
			final_dict["items"]={} #then we start filling the items part within the output dictionary
		else:
			item_number=k.split()[1].strip("[]: ")
			tmp_dict={}
			element_dict={}
			element_list=[]
			tier_grouped=[(key,[v[1:] for v in list(group)]) for key,group in groupby(grp,lambda x:x[0])] #we group the key-value pairs for the current tier/item, by element
			tier_type=""
			for tk, tgrp in tier_grouped:
				#print tk, len(tgrp), tgrp[:10]
				if tk=="": #the outside information of the tier, without going into the elements
					for t0,t1 in tgrp:
						tmp_dict[t0]=t1
						if t0.startswith("points"): tier_type="points" #given these outside info, if one of the keys start with points, it is a points tier
						if t0.startswith("intervals"): tier_type="intervals" #otherwise, it is an interval tier
				else:
					element_number=tk.split()[1].strip("[]: ") #we get the element number
					local_dict=dict(iter(tgrp)) #and create a local dict for element data

					element_dict[element_number]=local_dict #we update the element dictionary with the local element dictionary
					local_dict["id"]=element_number #for the option that we want to keep the elements ordered, we add another key to the local dict to keep the id of the element
					element_list.append(local_dict) #and we put it in the ordered list of elements

			if not order_elements: #then we decide if we want the elements in a dicionary e.g. our_dict[iten_number][element_number]={"xmin":20,"xmax":21}
				if tier_type=="points": tmp_dict["points"]=element_dict #depending in the type of elements, we update the tmp_dict
				if tier_type=="intervals": tmp_dict["intervals"]=element_dict
			else: #or we want it an ordered list e.g. our_dict[iten_number]=[{"id":15,"xmin":20,"xmax":21},{"id":16,"xmin":21,"xmax":22}]
				if tier_type=="points": tmp_dict["points"]=element_list
				if tier_type=="intervals": tmp_dict["intervals"]=element_list

			
			final_dict["items"][item_number]=tmp_dict #and finally we update the final dict with the tmp dict
	return final_dict


def textgrid_2_json(input_fpath,out_fpath,order_elements=False): #convert the input textgrid file into json file
	cur_dict=textgrid_2_dict(input_fpath,order_elements)
	json_content=json.dumps(cur_dict)
	#json_content=json_content.replace("{","\n{") #later we can include multiline features for ease of visual inspection
	#json_content=json_content.replace(",",",\n")
	#json_content=json_content.replace("\n \n","\n")
	#json_content=json_content.replace("\n\n","\n")
	#json_content=json_content.strip()
	fopen=open(out_fpath,"w")
	fopen.write(json_content)
	fopen.close()


if __name__=="__main__":
	print argv
	order_elements=False
	if len(argv)<3:
		print "Usage: textgrid_lib.py /input/directory/path/file.textgrid /output/directory/file.json -order"
		print "hint: -order is optional, the default is that elements (points/intervals) are in unordered dictionary, so if you specify -order they are in an ordered list"
	else:
		src_fpath=argv[1]
		trg_fpath=argv[2]
		if "-order" in argv: order_elements=True
		textgrid_2_json(src_fpath,trg_fpath,order_elements)
		print "converted %s to %s successfully!"%(src_fpath,trg_fpath)

	#praat_dir="autobi_out"
	#fname="sw2010.B.autobi.TextGrid"
	#fpath=os.path.join(praat_dir,fname)
	#fpath="test.textgrid"
	#out_fpath=fpath+".json"
	#our_final_dict=textgrid_2_dict(fpath,elements_as_dict=False)
	#textgrid_2_json(fpath,out_fpath,elements_as_dict=False)


#for f in our_final_dict:
#	if f=="items": continue
#	print ">>>", f, our_final_dict[f]

#for f in our_final_dict["items"]:
#	cur_elements=our_final_dict["items"][f].get("points",[])+our_final_dict["items"][f].get("intervals",[])
#	print ">>>", f, len(cur_elements)
#	for a in cur_elements:
#		print a
	
	#print '-----'
