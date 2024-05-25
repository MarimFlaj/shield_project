import os
from django.shortcuts import get_object_or_404, render
import random
from django.shortcuts import  redirect, render 
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.http import FileResponse, HttpResponse, JsonResponse, QueryDict
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as django_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils import timezone
from shield.forms import DepartmentForm, RegisterForm, SendingTrainingForm, SendingURlsForm, TrainingPackageForm, UrlForm
from shield.helper import update_secure_urls
from shield.models import DepartmentModel, SendingTrainingModel, SendingURlsModel, TrainingPackage, Url, User, send_email
from django.conf import settings

from django.contrib.auth import views as auth_views


# Create your views here.

class LoginView(auth_views.LoginView):
    frm_class=RegisterForm
    def get(self, request, *args, **kwargs):
        return render(request,'login_register.html',{"form":self.frm_class})

        
class RegisterView(View):
    form_class=RegisterForm
    def get(self, request, *args, **kwargs):
        return render(request,'register.html',{"form":self.form_class})

    def post(self,request,*args,**kwargs):
        if request.POST.get('login'):
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            #print(user,"ueeeeeeeeeeeeeeeeeeeeeee")
            if user is not None:
                django_login(request, user)
                return JsonResponse({'status': '1', 'message': 'Login successful'})
            else:
                msg=_("Incorrect data Please check your username and password")
                return JsonResponse({'status': '0', 'message': msg})
            
        elif request.POST.get('register'):   
            
            form_data = request.POST.copy()  # يتم نسخ بيانات الطلب إلى كائن قابل للتعديل

            form_data['phishing_awareness']='aware'
            form = self.form_class(form_data)
            if form.is_valid():
                obj = form.save(commit=False)
                pwd=obj.password
                
                obj.password=None
                obj.set_password(pwd)
                obj.last_update=timezone.now()
                #print("dddddddddddddddddddd")
                obj.save()
                msg=_("Added successfully")
                
               
                
                return JsonResponse({'status':'1','msg':msg})
            else:
                #print(form.errors,"ssssssssssssssssssssssssss")
                msg=_(str(form.errors))
                return JsonResponse({'status': '0', 'msg': msg , 'errors': form.errors})
            

class UsersJson(BaseDatatableView):
    model = User
    columns = [
        "username",
        "email",
        "Department",
        "gander",
        "phishing_awareness",
        "last_update",
        ] 
    
    fk_columns=[
        'Department'
        ]
    action_col = [
        ]
    
    def get_initial_queryset(self):
        return self.model.objects.filter(is_superuser=False)
    
    def filter_queryset(self, qs):
        from django.db.models import Q

        columns = self._columns
        if not self.pre_camel_case_notation:
            search = self._querydict.get("search[value]", None)
            q = Q()
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]
                    # print(column,"columncolumn")
                else:
                    column = data_field.replace(".", "__")

                if not column in self.action_col:
                    if not column in self.fk_columns:
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )
                    
            qs = qs.filter(q)
        return qs
    

        
class UserView(LoginRequiredMixin,View):
    template ='users.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, self.template)
            
        else:
            return redirect('https://www.google.com/')


class UrlJson(BaseDatatableView):
    model = Url
    columns = [
        # "url_id",
        "name",
        "description",
        "type",
        "del",
        ] 
    fk_columns=[]
    action_col = [

        'del',
        ]
    
    def get_initial_queryset(self):
        return self.model.objects.all()
    
    def render_column(self, row, column):
        if column == "del":
            text=_("Delete Contact")
            action ="""<a class="group_function" onclick="javascript:deleteContact({0});" title="{1}"><i class="fa fa-trash" aria-hidden="true" style="color: #757575;font-size: 20px;"></i></a>""".format(row.url_id,text)
            return action
        else:
            # For other columns, return the default rendering
            return super().render_column(row, column)

    def filter_queryset(self, qs):
        from django.db.models import Q

        columns = self._columns
        if not self.pre_camel_case_notation:
            search = self._querydict.get("search[value]", None)
            q = Q()
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]
                    # print(column,"columncolumn")
                else:
                    column = data_field.replace(".", "__")

                if not column in self.action_col:
                    if not column in self.fk_columns:
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )
                    
            qs = qs.filter(q)
        return qs
    
 
class UrlView(LoginRequiredMixin,View):
    template ='urls.html'
    form_class=UrlForm

    def get(self, request, *args, **kwargs):
        #print(request.GET.keys(),"sssssssssssssssssssssssss")

        if request.user.is_superuser:
            return render(request, self.template)
            
        else:
            return redirect('https://www.google.com/')

    def post(self,request,*args,**kwargs):
        if request.POST.get('save_new'):
            
            msg=_("Added successfully")
            form_data = request.POST.copy()
            form = self.form_class(form_data)
        
            if form.is_valid():
                obj = form.save(commit=False)
                
                obj.save()
                if obj.type=="secure":
                    update_secure_urls(obj,SecureUrlView)
                elif obj.type=="unsecure":
                    update_secure_urls(obj,UnSecureUrlView)
                # html_table=self.generate_html_table(request)
                return JsonResponse({'status':'1','msg':msg,})
                
            else:
                #print(form.errors,"ssssssssssssssssssssssssss")
                msg=_(str(form.errors))
                return JsonResponse({'status': '0', 'msg': msg , 'errors': form.errors})
        
    def delete(self,request,*args,**kwargs):
        id = int(QueryDict(request.body).get('id'))
        obj = get_object_or_404(Url,pk = id)
        obj.delete()
        msg=_("Deleted successfully")
        # html_table=self.generate_html_table(request)
        return JsonResponse({'status':'success','msg':msg})
    

class TrainingPackageJson(BaseDatatableView):
    model = TrainingPackage
    columns = [
        "Name",
        "description",
        "type",
        "train_file",
        "del",
        ] 
    fk_columns=[]
    action_col = [
        'del',
        ]
    def get_initial_queryset(self):
        return self.model.objects.all()
    
    def render_column(self, row, column):
        if column == "train_file":
            action ="""{1}  <a class="group_function" onclick="javascript:downloadRecord({0});" title="Download"><i class="fa fa-download" aria-hidden="true" style="font-size: 20px;color:#0087F7"></i></a>""".format(row.t_id,str(row.train_file))
            return action
        elif column == "del":
            text=_("Delete")
            action ="""<a class="group_function" onclick="javascript:deleteContact({0});" title="{1}"><i class="fa fa-trash" aria-hidden="true" style="color: #757575;font-size: 20px;"></i></a>""".format(row.t_id,text)
            return action
        else:
            # For other columns, return the default rendering
            return super().render_column(row, column)
    
    def filter_queryset(self, qs):
        from django.db.models import Q

        columns = self._columns
        if not self.pre_camel_case_notation:
            search = self._querydict.get("search[value]", None)
            q = Q()
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]
                    # print(column,"columncolumn")
                else:
                    column = data_field.replace(".", "__")

                if not column in self.action_col:
                    if not column in self.fk_columns:
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )
                    elif column=='grp_id__grp_name':
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )

            qs = qs.filter(q)
        return qs
    


class TrainingPackageView(LoginRequiredMixin,View):
    template ='training.html'
    form_class=TrainingPackageForm

    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return render(request, self.template)
            
        else:
            return redirect('https://www.google.com/')

    def post(self,request,*args,**kwargs):
        if request.POST.get('save_new'):
        
            msg=_("Added successfully")
            form_data = request.POST.copy()
            form_data['train_file']=request.FILES['train_file']
            form = self.form_class(form_data)
            
            #print(form,"SSSSSSSSSSSSSSSSSSSSS",request.FILES['train_file'])
            if form.is_valid():
                obj = form.save(commit=False)
                obj.train_file=request.FILES['train_file']
                obj.save()
                
                return JsonResponse({'status':'1','msg':msg,})
                
            else:
                #print(form.errors,"ssssssssssssssssssssssssss")
                msg=_(str(form.errors))
                return JsonResponse({'status': '0', 'msg': msg , 'errors': form.errors})
        
        elif request.POST.get('downloadFile'):
            return self.download_training_file(request)

    def download_training_file(self,request):
        
        save_file=TrainingPackage.objects.filter(t_id=request.POST.get('id')).last()
        response = FileResponse(save_file.train_file,as_attachment=True)
        return response



    def delete(self,request,*args,**kwargs):
        id = int(QueryDict(request.body).get('id'))
        obj = get_object_or_404(TrainingPackage,pk = id)
        obj.delete()
        msg=_("Deleted successfully")
        # html_table=self.generate_html_table(request)
        return JsonResponse({'status':'success','msg':msg})
    

class DepartmentJson(BaseDatatableView):
    model = DepartmentModel
    columns = [
        "number",
        "name",
        "del",
        ] 
    fk_columns=[]
    action_col = [
        
        'del',
        ]
    
    def get_initial_queryset(self):
        return self.model.objects.all()
    
    def render_column(self, row, column):
        if column == "del":
            text=_("Delete")
            action ="""<a class="group_function" onclick="javascript:deleteContact({0});" title="{1}"><i class="fa fa-trash" aria-hidden="true" style="color: #757575;font-size: 20px;"></i></a>""".format(row.number,text)
            return action
        else:
            # For other columns, return the default rendering
            return super().render_column(row, column)
        
    def filter_queryset(self, qs):
        from django.db.models import Q

        columns = self._columns
        if not self.pre_camel_case_notation:
            search = self._querydict.get("search[value]", None)
            q = Q()
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]
                    # print(column,"columncolumn")
                else:
                    column = data_field.replace(".", "__")

                if not column in self.action_col:
                    if not column in self.fk_columns:
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )
                    elif column=='grp_id__grp_name':
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )

            qs = qs.filter(q)
        return qs
    


class DepartmentsView(LoginRequiredMixin,View):
    template ='department.html'
    form_class=DepartmentForm

    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return render(request, self.template)
            
        else:
            return redirect('https://www.google.com/')

    def post(self,request,*args,**kwargs):
        if request.POST.get('save_new'):
        
            msg=_("Added successfully")
            form_data = request.POST.copy()
            form = self.form_class(form_data)
            

            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                
                return JsonResponse({'status':'1','msg':msg,})
                
            else:
                #print(form.errors,"ssssssssssssssssssssssssss")
                msg=_(str(form.errors))
                return JsonResponse({'status': '0', 'msg': msg , 'errors': form.errors})


    def delete(self,request,*args,**kwargs):
        id = int(QueryDict(request.body).get('id'))
        obj = get_object_or_404(DepartmentModel,pk = id)
        obj.delete()
        msg=_("Deleted successfully")
        return JsonResponse({'status':'success','msg':msg})
    
class ReportView(LoginRequiredMixin,View):
    template ='report.html'
    form_class=DepartmentModel

    def get(self, request, *args, **kwargs):
        
        if request.user.is_superuser:
            if request.GET.get("details"):
                id=request.GET.get("id")
                data=User.objects.filter(is_superuser=False,Department__number=id)
                training_package=len(TrainingPackage.objects.all())
                all_users_len=len(data)
                ware_users_len=len(data.filter(phishing_awareness="aware",Department__number=id))
                unaware_users_len=len(data.filter(phishing_awareness="unaware",Department__number=id))
                return JsonResponse({
                    'status':'1',
                    'training_package':training_package,
                    "all_users_len":all_users_len,
                    "ware_users_len":ware_users_len,
                    "unaware_users_len":unaware_users_len
                    }
                    )


            data=DepartmentModel.objects.all()
            return render(request, self.template,{"data":data})
        
            
        else:
            return redirect('https://www.google.com/')



from datetime import datetime, timedelta
from django.db.models import Q

def chart_api(request):
    current_date = datetime.now()

    data_list=[]
    data_list2=[]
    data_list3=[]
    data_list.append(current_date.strftime("%B %Y"))
    queryset = User.objects.filter(
            Q(last_update__year=current_date.year) &
            Q(last_update__month=current_date.month)&
        Q(phishing_awareness="aware")
        )
    data_list2.append(len(queryset))
    queryset = User.objects.filter(
            Q(last_update__year=current_date.year) &
            Q(last_update__month=current_date.month)&
        Q(phishing_awareness="unaware")
        )
    data_list3.append(len(queryset))
    # طباعة الشهور الـ 12 السابقة
    for i in range(1, 12):
        previous_month = current_date - timedelta(days=current_date.day)
        previous_month -= timedelta(days=1)
        current_date = previous_month
        if current_date.strftime("%B %Y") in data_list:
            continue
        else:
            data_list.append(current_date.strftime("%B %Y"))
            ware_users = User.objects.filter(
                Q(last_update__year=current_date.year) &
                Q(last_update__month=current_date.month)&
                Q(phishing_awareness="aware")
            )
            unaware_users = User.objects.filter(
                Q(last_update__year=current_date.year) &
                Q(last_update__month=current_date.month)&
                Q(phishing_awareness="unaware")
            )
        
            data_list2.append(len(ware_users))
            data_list3.append(len(unaware_users))
    data_list.reverse()
    data_list2.reverse()
    data_list3.reverse()
    return JsonResponse({'status':'1','data_list2':data_list2,"data_list":data_list,"data_list3":data_list3})

class SystemOverView(LoginRequiredMixin,View):
    template ='system_over.html'
    form_class=DepartmentModel

    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            data=User.objects.filter(is_superuser=False)
            training_package=len(TrainingPackage.objects.all())
            all_users_len=len(data)
            ware_users_len=len(data.filter(phishing_awareness="aware"))
            unaware_users_len=len(data.filter(phishing_awareness="unaware"))
            return render(request, self.template,
                          {
                              "data":data,
                              "all_users_len":all_users_len,
                              "ware_users_len":ware_users_len,
                              "unaware_users_len":unaware_users_len,
                              "training_package":training_package,
                           })
            
        else:
            return redirect('https://www.google.com/')


class SecureUrlView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/')
        else:
            return redirect('https://www.google.com/')
            
class UnSecureUrlView(LoginRequiredMixin,View):
    def get_template(self,template):
        if template=='fb':
            temp='fb.html'
        elif template=='sbl':
            temp='sbl.html'
        elif template=='unv':
            temp='unv.html'
        return temp
    
    def get(self, request, *args, **kwargs):
        print(request.user.is_superuser,"request.user.is_superuser")
        if not request.user.is_superuser:
            user=request.user
            user.phishing_awareness="unaware"
            user.last_update=timezone.now()
            user.save()
            
            template = kwargs.get('template', None)
            if template is not None:
                ret_val=self.get_template(template)
                if ret_val:
                    return render(request, ret_val)
                
            else:
                return HttpResponse("No value passed!")
                return redirect('https://www.google.com/')
        else:
            return redirect('/')

class SendingURlsJson(BaseDatatableView):
    model = SendingURlsModel
    columns = [
        "URL_ID",
        "send_to",
        "U_ID",
        "time",
        ]
    fk_columns=[

        'URL_ID',
        'U_ID',
    ]
    action_col = [
        
        ]
    
    def get_initial_queryset(self):
        return self.model.objects.all()
    
    def render_column(self, row, column):
        if column == "U_ID":
            if row.send_to=="user":
                return row.U_ID.username
            elif row.send_to=="department":
                return row.Department.name
        if column == "time":
            
            return row.time.strftime("%Y-%m-%d %H:%M:%S")  
        else:
            # For other columns, return the default rendering
            return super().render_column(row, column)
    
    def filter_queryset(self, qs):
        from django.db.models import Q

        columns = self._columns
        if not self.pre_camel_case_notation:
            search = self._querydict.get("search[value]", None)
            q = Q()
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]
                    # print(column,"columncolumn")
                else:
                    column = data_field.replace(".", "__")

                if not column in self.action_col:
                    if not column in self.fk_columns:
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )
                    elif column=='grp_id__grp_name':
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )

            qs = qs.filter(q)
        return qs
    

class SendingURlsView(LoginRequiredMixin,View):
    template ='sending_urls.html'
    form_class=SendingURlsForm

    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return render(request, self.template,{"form":self.form_class})
            
        else:
            return redirect('https://www.google.com/')

    def post(self,request,*args,**kwargs):
        if request.POST.get('save_new'):
            
            msg=_("Added successfully")
            form_data = request.POST.copy()
            form = self.form_class(form_data)
        
            form_data['time']=timezone.now()

            if form.is_valid():
                obj = form.save(commit=False)
                if not obj.U_ID and not obj.Department and obj.send_to!="all_users":
                    msg=_("Select User or Department ")
                    
                    return JsonResponse({'status': '2', 'msg': msg ,})

                obj.save()
                
                return JsonResponse({'status':'1','msg':msg,})
                
            else:
                #print(form.errors,"ssssssssssssssssssssssssss")
                msg=_(str(form.errors))
                return JsonResponse({'status': '0', 'msg': msg , 'errors': form.errors})

class SendingTrainingJson(BaseDatatableView):
    model = SendingTrainingModel
    columns = [
        "Train_ID",
        "send_to",
        "U_ID",
        "time",
        ]
    fk_columns=[

        'Train_ID',
        'U_ID',
    ]
    action_col = [
        
        ]
    
    def get_initial_queryset(self):
        return self.model.objects.all()
    
    def render_column(self, row, column):
        if column == "U_ID":
            if row.send_to=="user":
                return row.U_ID.username
            elif row.send_to=="department":
                return row.Department.name
        if column == "time":
            
            return row.time.strftime("%Y-%m-%d %H:%M:%S")  
        else:
            # For other columns, return the default rendering
            return super().render_column(row, column)

    def filter_queryset(self, qs):
        from django.db.models import Q

        columns = self._columns
        if not self.pre_camel_case_notation:
            search = self._querydict.get("search[value]", None)
            q = Q()
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]
                    # print(column,"columncolumn")
                else:
                    column = data_field.replace(".", "__")

                if not column in self.action_col:
                    if not column in self.fk_columns:
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )
                    elif column=='grp_id__grp_name':
                        if search and col["searchable"]:
                            # Apply istartswith only to string fields
                            if isinstance(column, str):
                                q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                        if col["search.value"]:
                            # Filter only string fields
                            if isinstance(column, str):
                                qs = qs.filter(
                                    **{"{0}__{1}".format(column, filter_method): col["search.value"]}
                                )

            qs = qs.filter(q)
        return qs
    
    

class SendingTrainingView(LoginRequiredMixin,View):
    template ='sending_training.html'
    form_class=SendingTrainingForm

    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return render(request, self.template,{"form":self.form_class})
            
        else:
            return redirect('https://www.google.com/')

    def post(self,request,*args,**kwargs):
        if request.POST.get('save_new'):
            
            msg=_("Added successfully")
            form_data = request.POST.copy()
            form = self.form_class(form_data)
        
            form_data['time']=timezone.now()

            if form.is_valid():
                obj = form.save(commit=False)
                if not obj.U_ID and not obj.Department and obj.send_to!="all_users":
                    msg=_("Select User or Department ")
                    
                    return JsonResponse({'status': '2', 'msg': msg ,})

                obj.save()
                
                return JsonResponse({'status':'1','msg':msg,})
                
            else:
                #print(form.errors,"ssssssssssssssssssssssssss")
                msg=_(str(form.errors))
                return JsonResponse({'status': '0', 'msg': msg , 'errors': form.errors})

class MyProfile(LoginRequiredMixin,View):
    template ='page-user.html'
    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return render(request, self.template)
            
        else:
            return redirect('https://www.google.com/')
        
    def post(self,request,*args,**kwargs):
        if request.POST.get('update'):
            try:
                msg=_("Update successfully")
                form_data = request.POST.copy()

                user_ob=User.objects.filter(u_id=request.user.u_id).last()
                user_ob.f_name = form_data['f_name']
                user_ob.f_name = form_data['f_name']
                user_ob.m_name = form_data['m_name']
                user_ob.l_name = form_data['l_name']
                user_ob.username = form_data['username']
                user_ob.email = form_data['email']
                user_ob.gander = form_data['gander']
                user_ob.save()
                return JsonResponse({'status':'1','msg':msg,})
                
            except Exception as e:
                print(e,"eeeeeeeeeeeeeeeeeeeeeer")
                return JsonResponse({'status': '0', 'msg': msg , 'errors': str(e)})


import random
import string

def generate_random_password(length=12, include_uppercase=True, include_lowercase=True, include_digits=True, include_special_chars=True):

    characters = ''
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_special_chars:
        characters += string.punctuation

    # Remove any duplicate characters from the characters string
    characters = list(set(characters))

    # Ensure there are at most two special characters
    special_chars = random.sample(string.punctuation, min(2, length - 10))
    characters.extend(special_chars)

   

    # Generate the password
    random.shuffle(characters)
    password = ''.join(characters[:length])
    return password   


class ForgetPassword(View):
    template ='forget_pass.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template)

            
    def post(self,request,*args,**kwargs):
        
        msg=_("Sent successfully To your email")
        form_data = request.POST.copy()

        user_ob=User.objects.filter(email=form_data['email']).last()
        if user_ob :
            pwd=generate_random_password()
        
            user_ob.password=None
            user_ob.set_password(pwd)
            user_ob.save()
            recipient_list=[form_data['email']]
            message=f"Dear \n Your new password is {pwd} \n Thank you"
            subject="Reset Password"
            send_email(recipient_list,message,subject)
            return JsonResponse({'status':'1','msg':msg,})
        else:
            msg=_("User Not found")
            return JsonResponse({'status':'0','msg':msg,})
    
        