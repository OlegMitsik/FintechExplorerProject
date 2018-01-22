import json

def Generate_Taxonomy_JSON(DB_Taxonomy):
    Root_Node_Index = Get_Index_By_ID(DB_Taxonomy, 1)
    Res_Dict = Create_Taxonomy_Dict(DB_Taxonomy, DB_Taxonomy[Root_Node_Index])
    return json.dumps(Res_Dict)

def Create_Taxonomy_Dict(DB_Taxonomy, DB_Node):
    Dict = {"id": DB_Node[0], "name": DB_Node[2], "data": {"isCategory": DB_Node[3], "description": DB_Node[4]},"children": []}
    Children_list = Get_Children_IDs(DB_Taxonomy, DB_Node[0])
    for Child in Children_list:
        Child_Index = Get_Index_By_ID(DB_Taxonomy, Child)
        Dict["children"].append(Create_Taxonomy_Dict(DB_Taxonomy, DB_Taxonomy[Child_Index]))
    return Dict

def Get_Children_IDs(DB_Taxonomy, parent_ID):
    outp = []
    for row in DB_Taxonomy:
        if (row[1] == parent_ID):
            outp.append(row[0])
    return outp

def Get_Index_By_ID(DB_Taxonomy, ID_num):
    for index, item in enumerate(DB_Taxonomy):
        if (item[0] == ID_num):
            return index
