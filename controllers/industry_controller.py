from flask import render_template

class IndustryController:

    def __init__(self,industryCrosstableService,template):
        self.industryCrosstableService = industryCrosstableService
        self.template = template

        self.user_id = 3

    def change_user(self,request):
        self.user_id = request.args.get('user')
        return self.dispatch(request)

    def dispatch(self,request):
        user_industries,crosstable = self.industryCrosstableService.get_by_user(self.user_id)
        return render_template(self.template,user_industries=user_industries,crosstable=crosstable,user=self.user_id)

    def add(self,request):
        name = request.form.get('new_industry')
        if name is not None and name != '':
            if not self.industryCrosstableService.user_have_industry(user_id=self.user_id,name=name):
                self.industryCrosstableService.add(self.user_id,name)
        return self.dispatch(request)

    def delete(self,request):
        try:
            raw_id = request.form.get('industry_id')
            print("rawid" ,raw_id)
            id = int(raw_id)
            if id is not None:
                self.industryCrosstableService.delete(id,self.user_id)
        except Exception as problem:
            print(problem)
            pass
        return self.dispatch(request)

    def save_relations(self,request):
        self.industryCrosstableService.save_relations(request.form,self.user_id)
        return self.dispatch(request)







