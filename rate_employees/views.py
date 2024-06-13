

from django.http import HttpResponse
from django.shortcuts import render, redirect
from rate_employees.models import Employee, Evaluation, Designation
from . registrationForm import EmployeeRegistration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from . import petro


# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request,'employees/homePage.html')

@login_required(login_url='login')
def employees_info(request):
    employee = Employee.objects.all()
    return render (request, 'employees/evaluation.html', {'emp': employee} )

@login_required(login_url='login')
def mark_employees(request):
    return render (request, 'employees/mark.html')

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == "POST":
            fm = UserCreationForm(request.POST)
            if fm.is_valid():
                fm.save()
                print("this post from registration")
                return redirect('home')
        else:
            fm = UserCreationForm()
        return render(request,'employees/registration.html',{'form': fm})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                messages.info(request, 'Username or Password is incorrect')

        return render(request,'employees/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def showProfileData(request):
    if request.method == 'POST':
        print("request post")
        print(request.POST)
        fm = EmployeeRegistration(request.POST)

        if fm.is_valid():
            mydata = Employee.objects.filter(enothi_id = request.user)
            if mydata.exists():
    
                myProfileData = Employee.objects.get(enothi_id = request.user)
                #print(" My Objects ",myProfileData[0])
                myProfileData.ename = request.POST['name']
                myProfileData.eemail = request.POST['email']
                myProfileData.empid = request.POST['empid']
                myProfileData.edesignation = request.POST['designation']
                myProfileData.esection = request.POST['section']
                myProfileData.edept = request.POST['department']
                myProfileData.edivision = request.POST['division']
                myProfileData.edirectorate = request.POST['directorate']
                myProfileData.save()
                return redirect('home')

            #print(fm)
            print("This is POST statement")
            print(request.POST['name'])
            name = request.POST['name']
            email = request.POST['email']
            enothi_id = request.user
            empid = request.POST['empid']
            designation = request.POST['designation']
            section = request.POST['section']
            department = request.POST['department']
            division = request.POST['division']
            directorate = request.POST['directorate']

            new_emp = Employee(empid = empid, enothi_id = enothi_id , ename = name, eemail = email, edesignation = designation, edept = department, esection = section, edivision = division, edirectorate = directorate)
            #print(fm.cleaned_data)
            new_emp.save()
            return redirect('home')
        #else if request.POST['enothi_id']:
        else:
            print("not valid enothi_id ",request.user)
            print("enothi_id from post ",request.POST['enothi_id'])
            #print(fm)

    else: 
        fm = EmployeeRegistration()
        fm.initial['enothi_id'] = request.user
        user_id = request.user
        mydata = Employee.objects.filter(enothi_id=request.user).values()
        if mydata.exists():
            print("mydata exists!!")
            print(request.POST)
            fm.initial['name'] = mydata[0]['ename']
            fm.initial['email'] = mydata[0]['eemail']
            fm.initial['empid'] = mydata[0]['empid']
            fm.initial['designation'] = mydata[0]['edesignation']
            fm.initial['section'] = mydata[0]['esection']
            fm.initial['department'] = mydata[0]['edept']
            fm.initial['division'] = mydata[0]['edivision']
            fm.initial['directorate'] = mydata[0]['edirectorate']
            

            designations = Designation.objects.all()
            
            context = {
                'myProfileData': mydata,
                'form': fm,
                'enothi_id':user_id,
                'designationData': designations
                }
            #return HttpResponse(template.render(context, request))
            print("This is my data",mydata[0]['ename'])
            print("This is Employee Enothi ",fm['enothi_id'])
            return render(request,'employees/profile.html',context)
    designations = Designation.objects.all()
    context = {
                'form':fm,
                'enothi_id':user_id,
                'designationData': designations
                }
    return render(request,'employees/profile.html',context)

@login_required(login_url='login')
def select_evaluatee(request): 
    if request.method == 'POST':
        print(request.POST['employee'][1:5]) # need to check
        evaluatee_empid = int(request.POST['employee'][1:5]) #employee id must be of 4 digits
        evaluatee = Employee.objects.filter(empid = evaluatee_empid).values()
        #print("Select Evaluatee")
        #print(Designation.objects.filter(desigid = evaluatee[0]['edesignation']).values()[0]['designame'])
        #evaluatee_designation = Designation.objects.filter(desigid = evaluatee[0]['edesignation']).values()[0]['designame']
        print(evaluatee[0]['edesignation'])
        context = {
                'evaluateeeData': evaluatee,
                
                }
        return redirect('evaluate',emp_id = evaluatee_empid)
    else:
        employees = Employee.objects.all()
        #serialized_data = serialize("json", employees)
        context = {
                'employeeData': employees
                }
        return render(request,'employees/select_evaluatee.html',context) 


@login_required(login_url='login')
def evaluate(request, emp_id):
    if request.method == 'POST':
        print("Evaluate Post Method ",request.user)
        for key, value in request.POST.items():
            print('Key: %s' % (key) ) 
            # print(f'Key: {key}') in Python >= 3.7
            print('Value %s' % (value) )
            # print(f'Value: {value}') in Python >= 3.7
        #print(request.GET['employee'][1:5]) # need to check
        print("Data type check ",type(request.user.id))
        print("Data type check ",(request.user))
        evaluateeid = int(request.POST['evaluateeid'])
        evaluatorid =  Employee.objects.filter(enothi_id = int(request.user.username)).values()[0]['empid']
        secDeptEv = int(request.POST['secDept'])
        commEv = int(request.POST['committee'])
        behavEv = int(request.POST['behaviour'])
        comid = 1 # need to be modified
        new_eval = Evaluation(evaluateeid = evaluateeid, evaluatorid = evaluatorid , secDeptEv = secDeptEv, commEv = commEv, behavEv = behavEv, comid = comid)
        #print(fm.cleaned_data)
        new_eval.save()
        return redirect('home')
    evaluatee_empid = emp_id #employee id must be of 4 digits
    evaluatee = Employee.objects.filter(empid = evaluatee_empid).values()[0]
    print("Evaluate function")
    print(evaluatee)
       
    context = {
                'evaluateeData': evaluatee,
                'evaluateeDesignation' : Designation.objects.filter(desigid = evaluatee['edesignation']).values()[0]['designame']
                }
    print("test ",context['evaluateeData']['ename'])
    return render(request,'employees/evaluate.html',context)
        #return render(request,'employees/evaluate.html') 

@login_required(login_url='login')
def showReport(request):

    if request.method == 'POST':
        print("Report Post method called")
        print(request.POST)
        if request.POST['profile'] == "Back to Query":
            designations = Designation.objects.all()
            employees = Employee.objects.all()
            context = {
                'designationData': designations,
                'employeeData': employees
            }
            return render(request,'employees/query.html',context)
        
        elif request.POST['evalBased'] == "everyone" :
            print("Everyone's Evaluation")
            #print(type(int(request.POST['employee'][1:5])))
            #evaluatee_section = Employee.objects.filter(empid = int(request.POST['employee'][1:5])).values()[0]['esection']
            all_evals = Evaluation.objects.filter(evaluateeid = int(request.POST['employee'][1:5])).values()
            results = []
            #print(type(all_evals))
            #print("Evaluatee Section : ",evaluatee_section)

            
            for eval in all_evals:
                results.append(eval)
                print("Evaluator ID : ",eval['evaluatorid'])
                print(type(eval['evaluatorid']))
                evaluator_section = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]['esection']
               
            final_report = []
            #print(results)
            for eval in results:
                evaluator = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]
                print("Evaluator Info : ",evaluator['ename'])
                print("Section : ",petro.sections[int(evaluator['esection'])-1][1])
                print("SecDept Eval : ",petro.remarks[int(eval['secDeptEv'])-1][1])
                print("Committee Eval : ",petro.remarks[int(eval['commEv'])-1][1])
                print("Behavior Eval : ",petro.remarks[int(eval['behavEv'])-1][1])

                final_report.append({
                                  'evaluatee': Employee.objects.filter(empid = eval['evaluateeid']).values()[0]['ename'],
                                  'evaluator': evaluator['ename'], 
                                  'section': petro.sections[int(evaluator['esection'])-1][1],
                                  'secDeptEval' : petro.remarks[int(eval['secDeptEv'])-1][1],
                                  'comEval' : petro.remarks[int(eval['commEv'])-1][1],
                                  'behavEval': petro.remarks[int(eval['behavEv'])-1][1],
                                    }
                                  )
            print("final Report")
            print(final_report)
            context = {
                'report_data': final_report
                }
            
            return render(request,'employees/report.html',context)
        elif request.POST['evalBased'] == "secDept":
            print("Section or Department's evaluation")
            print(type(int(request.POST['employee'][1:5])))
            evaluatee_section = Employee.objects.filter(empid = int(request.POST['employee'][1:5])).values()[0]['esection']
            all_evals = Evaluation.objects.filter(evaluateeid = int(request.POST['employee'][1:5])).values()
            results = []
            print(type(all_evals))
            print("Evaluatee Section : ",evaluatee_section)

            
            for eval in all_evals:
                print("Evaluator ID : ",eval['evaluatorid'])
                print(type(eval['evaluatorid']))
                evaluator_section = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]['esection']
                if evaluatee_section == evaluator_section:
                    print("Matched!! This should be inserted")
                    results.append(eval)
                #print("Evaluator Section : " ,query_set[0]['esection'])
                
                #results.append(eval)
            final_report = []
            print(results)
            for eval in results:
                evaluator = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]
                print("Evaluator Info : ",evaluator['ename'])
                print("Section : ",petro.sections[int(evaluator['esection'])-1][1])
                print("SecDept Eval : ",petro.remarks[int(eval['secDeptEv'])-1][1])
                print("Committee Eval : ",petro.remarks[int(eval['commEv'])-1][1])
                print("Behavior Eval : ",petro.remarks[int(eval['behavEv'])-1][1])

                final_report.append({
                                  'evaluatee': Employee.objects.filter(empid = eval['evaluateeid']).values()[0]['ename'],
                                  'evaluator': evaluator['ename'], 
                                  'section': petro.sections[int(evaluator['esection'])-1][1],
                                  'secDeptEval' : petro.remarks[int(eval['secDeptEv'])-1][1],
                                  'comEval' : petro.remarks[int(eval['commEv'])-1][1],
                                  'behavEval': petro.remarks[int(eval['behavEv'])-1][1],
                                    }
                                  )
            print("final Report")
            print(final_report)
            context = {
                'report_data': final_report
                }
            
            return render(request,'employees/report.html',context)
        #remarks = Evaluation.objects.filter(secDeptEv = int(request.POST['remark'])).values()
        #remarks = Evaluation.objects.filter(secDeptEv = 4)
        #employee_list = []
        #remarks=[]
        
        #for remark in remarks:
        #    print(remark['evaluateeid'])
        #    evaluatee = Employee.objects.filter(empid = remark['evaluateeid']).values()[0]
        ##    print(evaluatee['ename'])
        #    print(evaluatee['edesignation'])
        #    print(evaluatee['edept'])
        #    print(evaluatee['edivision'])
        #    print(evaluatee['esection'])

            #print(remark['evaluatorid'])
        #    print(petro.departments[2][1])
        #    print("Done")
        #    employee_list.append({
        #                          'name': evaluatee['ename'], 
        #                          'section': petro.sections[int(evaluatee['esection'])-1][1],
        #                          'designation' : Designation.objects.filter(desigid = evaluatee['edesignation']).values()[0]['designame'],
        #                          'dept' : petro.departments[int(evaluatee['edept'])-1][1],
        #                          'division': petro.divisions[int(evaluatee['edivision'])-1][1],
        #                            }
        #                          )
            
        #print(type(int(request.POST['remark'])))
        #print(employee_list)
        context = {
                'report_data': final_report,
                }
        return render(request,'employees/report.html',context)
    
    designations = Designation.objects.all()
    employees = Employee.objects.all()
    context = {
                'designationData': designations,
                'employeeData': employees
            }
    return render(request,'employees/query.html',context)


@login_required(login_url='login')
def giveAward(request):
    if request.method == 'POST':

        print("checkkk!!!!!!!")
        print(request.POST['employee'])
        print(request.POST['permission'])
        return redirect('home')
        #return redirect('writeAwardDescription',emp_id = int(request.POST['employee']))
    employee = Employee.objects.all()
    return render (request, 'employees/award.html', {'employeeData': employee} )
    

@login_required(login_url='login')
def writeAwardDescription(request,emp_id):
    if request.method == 'POST':
        #print(request.POST['giveAward'])
        #print(request.POST['employee'])
        print("if from writeAwardDescription")
        
    print("get from write award")
    employee = Employee.objects.all()
    return render (request, 'employees/write_award_description.html', {'employeeData': employee} )
