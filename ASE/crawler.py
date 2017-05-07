from urllib.request import urlopen
import re
from .models import Course

def extract(course_info):
	course = {}
	pattern = '[^<]*?\">(.*?)</span>'
	result = re.search(pattern, course_info, re.DOTALL)
	if result:
		course['title'] = result.group(1)
	else:
		return course
	pattern = '[A-Z]+ *?[0-9]+'
	result = re.search(pattern, course['title'], re.DOTALL)
	if result:
		course['code'] = result.group(0)
		pattern = '[A-Z]+ *?[0-9:]+ *?(\w.*?)$'
		result = re.search(pattern, course['title'], re.DOTALL)
		course['name'] = result.group(1)

	pattern = '<p><span class=\"credits\">( *?([0-9\.]*) credits? \([0-9]*\-[0-9]*\-[0-9]*\) *?)</span></p>'
	result = re.search(pattern, course_info, re.DOTALL)
	if result:
		cred_LTP = result.group(1)
		pattern = '[0-9\.]*'
		course['credits'] = re.search(pattern, cred_LTP, re.DOTALL).group(0)
		pattern = '[0-9]*-[0-9]*-[0-9]*'
		course['LTP'] = re.search(pattern, cred_LTP, re.DOTALL).group(0)


	pattern = '<p><span class=\"prereq\">Pre-requisites:</span>(.*?)</p>'
	result = re.search(pattern, course_info, re.DOTALL)
	if result:
		course['prereq'] = result.group(1)
	pattern = '<p><span class=\"overlap\">Overlaps with:</span>(.*?)</p>'
	result = re.search(pattern, course_info, re.DOTALL)
	if result:
		course['overlap'] = result.group(1)

	pattern = '<br/><p>([^<]*?)$'
	result = re.search(pattern, course_info, re.DOTALL)
	course['contents'] = ""
	if result:
		course['contents'] = result.group(1)
	
	if 'code' not in course:
		return None

	try:
		credits = int(course['credits'])
		course['code'] = course['code'].replace(" ", "") # remove whitespaces in code e.g. COL 672 -> COL672
	except:
		return None

	return course

# crawl the website and update course info
def crawl_courses():
	response = urlopen("http://www.cse.iitd.ernet.in/cse/newcurriculum-contents/newcourses.html")
	html = response.read().decode('utf-8')
	pattern = '<p><span class=\"title\" id=\"(.*?)</p><br/><hr><br>'
	matches = re.findall(pattern, html, re.DOTALL)
	for s in matches:
		course = extract(s)
		if course is not None:
			entry = Course(code=course['code'], name=course['name'], credits=course['credits'], LTP=course['LTP'], contents=course['contents'])
			entry.save()