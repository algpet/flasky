
class IndustryCrosstableService:

    def __init__(self,industryDbService,industryRelationsDbService,industryCrosstableDefaultTemplateService):
        self.industryDbService = industryDbService
        self.industryRelationsDbService = industryRelationsDbService
        self.industryCrosstableDefaultTemplateService = industryCrosstableDefaultTemplateService

    def get_by_user(self,user_id):
        user_industries = self.industryDbService.getByUser(user_id)
        user_industry_relations = self.industryRelationsDbService.getByUser(user_id)
        crosstable = self.get_crosstable(user_industries,user_industry_relations)
        return user_industries,user_industry_relations,crosstable


    def get_crosstable(self,user_industries,user_industry_relations):
        crosstable = {}
        for item1 in user_industries:
            id1 = item1['id']
            crosstable[id1] = {}
            for item2 in user_industries:
                id2 = item2['id']
                crosstable[id1][id2] = 0

        for row in user_industry_relations:
            try:
                crosstable[row['industry1_id']][row['industry2_id']] = row['score']
            except Exception:
                pass
        return crosstable


    def get_template(self,user_id):
        own = self.get_by_user(user_id)
        if len(own[0]) != 0:
            return own
        template_user_id = self.industryCrosstableDefaultTemplateService.get_template_owner()
        template_industries,template_industry_relations,template_crosstable = self.get_by_user(template_user_id)

        name_to_id_map = {}
        for template_industry in template_industries:
            name_to_id_map[template_industry['name']] = template_industry['id']

        connection = self.industryDbService.connectionFactory.get_connection()
        for industry in template_industries:
            self.industryDbService.insert_full(user_id, industry['name'],industry['desc'],connection=connection)
        saved_industries = self.industryDbService.getByUser(user_id,connection)

        template_id_to_new_id_map = {}
        for saved_industry in saved_industries:
            template_id_to_new_id_map[name_to_id_map[saved_industry['name']]] = saved_industry['id']


        for entry in template_industry_relations:
            self.industryRelationsDbService.insert(template_id_to_new_id_map[entry['industry1_id']],
                                                   template_id_to_new_id_map[entry['industry2_id']],
                                                   entry['score'],user_id,
                                                   connection=connection)
        connection.commit()

        return self.get_by_user(user_id)



    def user_have_industry(self,user_id,name):
        user_industries = self.industryDbService.getByUser(user_id)
        for industry in user_industries:
            if industry['name'] == name:
                return True
        return False

    def get_by_id(self, id):
        return self.industryDbService.getById(id)

    def delete(self,id,user_id):
        industry = self.industryDbService.getById(id)
        if industry is not None and industry['user_id'] == user_id:
            print("we are here")
            self.industryDbService.delete(id)
            print("deleting for relationid",id)
            self.industryRelationsDbService.deleteByRelation(id)

        #return self.industryDbService.delete(id)

    def add(self,user_id,name):
        self.industryDbService.insert(user_id,name)



    def update(self,form_data,user_id):
        connection = self.industryDbService.connectionFactory.get_connection()

        entries = []
        for item in form_data:
            if item.startswith("name,"):
                entries.append({'id': item.split(',')[1], 'user_id': user_id, 'name': form_data[item],'desc': form_data[item.replace('name', 'desc')]})

        for entry in entries:
            self.industryDbService.update(entry['id'],entry['user_id'],entry['name'],entry['desc'],connection=connection)

        self.industryRelationsDbService.deleteByUser(user_id,connection=connection)
        for entry in form_data:

            if not entry.startswith("relation:"):
                continue

            score = int(form_data[entry])
            if score == 0:
                continue

            pair = self.get_relation_pair(entry)
            if pair[0] == pair[1]:
                continue

            self.industryRelationsDbService.insert(pair[0],pair[1],score,user_id,connection=connection)
        connection.commit()

    def get_relation_pair(self,form_name):
        data = form_name.split(":")[1]
        from_to = data.split(",")
        return [int(from_to[0]),int(from_to[1])]





