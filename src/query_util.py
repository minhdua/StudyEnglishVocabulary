import copy


class StringMapper:
    '''
        this class convert object to dictionary object with key is field name and value is values that filed
        if value is blank then not add that filed into dictionary
        function:
            init: pass object
            getMapperObject: return mapper Object converted from object
            getKeys: return list key getted from object
            getValues return list value getted from object
            getKeysToCSVString: return key list formated to csv string
            getValueToCSVString: return value list formated to csv string
    '''
    def __init__(self,object):
        self.object = object

    def cover(self,word):
        return '\"'+str(word)+'\"'

    def mapper_object(self):
        object_dict = self.object.__dict__
        mapper = {}
        for key in object_dict:
            if(object_dict[key]):
                mapper[key] = self.cover(object_dict[key])
        return mapper 

    def keys(self):
        keys = []
        object_dict = self.mapper_object()
        for key in object_dict:
            keys.append(key)
        return keys

    def values(self):
        values = []
        object_dict = self.mapper_object()
        for key in object_dict:
            values.append(object_dict[key])
        return values

    def keys_to_csv_string(self):
        keys = self.keys()
        return ','.join(keys)

    def values_to_csv_string(self):
        values = self.values()
        return ','.join(values)
    
    def equals_csv_string(self):
        equals = []
        object_dict = self.mapper_object()
        for key in object_dict:
            equals.append(self.equals_string(key))
        return ','.join(equals)

    def equals_string(self,key):
        try:
            object_dict = self.mapper_object()
            return key +'='+ object_dict[key]
        except KeyError as e:
            print (e)

    def greater_string(self,key):
        object_dict = self.mapper_object()
        return key +'>'+ object_dict[key]

    def lesser_string(self,key):
        object_dict = self.mapper_object()
        return key +'<'+ object_dict[key]

    def like_string(self,key):
        object_dict = self.mapper_object()
        return key +' like "%'+object_dict[key].replace('"','')+'%"'

    def condition_string(self,field):

        if(not isinstance(field,tuple)):
            field = (field,'equals')

        try:
            if(field[1] == 'greater'):
                return self.greater_string(field[0])
            elif(field[1] == 'lesser'):
                return self.lesser_string(field[0])
            elif(field[1] =='like'):
                return self.like_string(field[0])
            else:
                return self.equals_string(field[0])
        except KeyError as e:
            print (e)

class QueryBuilder:
    '''
        this class to build condition in query if condition not null
        return: string query if have at least one condition
                None if have not condition any
        constant query insert,update,delete,select
        function:
            insertBuilder: build query insert string
            updateBuilder: build query update string
            deleteBuilder: build query delete string
            selectBuilder: build query select string
    '''
    INSERT_QUERY = 'INSERT INTO {table} ({fields}) VALUES ({values})'
    UPDATE_QUERY = 'UPDATE {table} SET {mapperString}'
    DELETE_QUERY = 'DELETE FROM {table}'
    SELECT_QUERY = 'SELECT * FROM {table}'
    WHERE = ' WHERE '
    AND = ' AND '
    CONDITION = ' {condition} '
    END = ';'
    SORT_BY_UPDATE_DATE = ' ORDER BY date_create DESC '
    LIST_UNIT_LASTEST = 'SELECT * FROM listunitnearest'
    SELECT_VDTO_BY_UNIT = 'SELECT * FROM hacknao1500.vocabularydto_by_unit where unit_code=\'{}\';'
    

    def __init__(self,object,primaries=None,object_origin=None):
        self.table = type(object).__name__
        self.primaries = primaries
        self.set_object(object)
        self.set_object_origin(object_origin)

    def list_unit_builder(self,n):
        return self.LIST_UNIT_LASTEST +self.where_builder()+ ' limit {} '.format(n) + self.END

    def where_builder(self):
        where_string = ''
        if(self.primaries != None and len(self.primaries) > 0):
            ids = copy.deepcopy(self.primaries)
            object_mapper = self.object_origin_mapper
            for idx in ids:
                condition_string = object_mapper.condition_string(idx)
                if(condition_string):
                    if(where_string == ''):
                        where_string = condition_string
                    else:
                        where_string = where_string + self.AND + condition_string
        return (self.WHERE + where_string) if where_string != '' else ''

    def insert_builder(self):
        table = self.table
        fields = self.object_mapper.keys_to_csv_string()
        values = self.object_mapper.values_to_csv_string()
        return self.INSERT_QUERY.format(table=table,fields=fields,values=values) + self.END

    def update_builder(self):
        table = self.table
        mapper_string = self.object_mapper.equals_csv_string()
        return self.UPDATE_QUERY.format(table=table,mapperString=mapper_string) + self.where_builder() + self.END
    
    def delete_builder(self):
        table = self.table
        return self.DELETE_QUERY.format(table=table) + self.where_builder() + self.END

    def select_builder(self):
        table = self.table
        return    self.SELECT_QUERY.format(table=table) + self.where_builder() + self.SORT_BY_UPDATE_DATE+ self.END

    def general_info(self):
        return self.GENERAL_INFOR

    def set_object(self,object): 
        self.object = object
        self.object_mapper = StringMapper(object)

    def set_object_origin(self,object_origin):
        self.object_origin = object_origin
        if(object_origin == None):
            self.object_origin = self.object
        self.object_origin_mapper = StringMapper(self.object_origin)

    def select_vdto_by_unit_builder(self,unit_code):
        return self.SELECT_VDTO_BY_UNIT.format(unit_code)
