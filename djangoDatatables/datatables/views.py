from django.shortcuts import get_object_or_404, render
from django.shortcuts import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
import urllib3, json, datetime, pickle
from datetime import datetime
from django.conf import settings

def get1cdata(request):
#    import pudb; pudb.set_trace()
    if(request.GET.get('refresh-butt')):
        print(request.GET.get('dateStart'))
 
    http = urllib3.PoolManager()
    myHeaders = urllib3.util.make_headers(basic_auth='admin:admin')

    dateStartStr = request.GET.get('dateStart')
    dateEndStr = request.GET.get('dateEnd')
    print('Got dates - ',dateStartStr, ', ',dateEndStr,'.')
    
    date_format = '%m/%d/%Y'

    if dateStartStr and dateEndStr:      
        dateStart = datetime.strptime(request.GET.get('dateStart'), date_format)
        dateEnd = datetime.strptime(request.GET.get('dateEnd'), date_format)
    else:
        dateStart = timezone.now()
        dateEnd = timezone.now()

    encoded_body = json.dumps({
        "description": "Запрос отчёта",
        "partner": "Розничный покупатель",
        "dateStart": dateStart.strftime("%Y%m%d000000"),
        "dateEnd": dateEnd.strftime("%Y%m%d235959"),
    })
    
    
    res=http.request('POST', 'http://localhost:8881/db2023/hs/reportsService/reportsMain', headers=myHeaders,body=encoded_body)
    table1c = res.data.decode('utf-8-sig').replace(u'\u000D\u000A','')

#    tableFilePath = settings.BASE_DIR / 'datasource.pkl'
#    with open(tableFilePath, 'wb') as sourceTable:
#        pickle.dump(table1c, sourceTable)
#    sourceTable.close()
    
 #   import pudb; pudb.set_trace()
    
#    return render(request,'tables.html', {'queueList': res, 'type_id': type(res.json())})
    return render(request,'tables.html', {'table1c': table1c, 'type_id': type(table1c)})
