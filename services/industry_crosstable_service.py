
class IndustryCrosstableService:

    def __init__(self,industryDbService,industryRelationsDbService):
        self.industryDbService = industryDbService
        self.industryRelationsDbService = industryRelationsDbService

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
        print("delete industry",industry,"for userid",user_id)
        print(industry is not None)
        print(industry['user_id'] == user_id)
        print(type(industry['user_id']))
        print(type(user_id))
        if industry is not None and industry['user_id'] == user_id:
            print("we are here")
            self.industryDbService.delete(id)
            print("deleting for relationid",id)
            self.industryRelationsDbService.deleteByRelation(id)

        #return self.industryDbService.delete(id)

    def add(self,user_id,name):
        self.industryDbService.insert(user_id,name)

    def save_relations(self,form_data,user_id):

        connection = self.industryDbService.connectionFactory.get_connection()
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





