# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
@auth.requires_membership('import')
def index():
    #TODO: Create a results page for importing csv, nessus, openvas, and nmap
    import importlib
    if type(modulelist) is not dict:
        return
    for module,attributes in modulelist:
        if "IMPORT" in attributes['FUNCTIONS'] and attributes['DISABLED'] == False:
            importlib.import_module(module)
    form = SQLFORM.factory(Field(" ", default=" ", writable=False),
                           Field("User_Name", 'string', required=True, default=auth.user.username, requires=IS_NOT_EMPTY(),writable=False),
                           Field('User_IP','string', required=True, writable=False, default=request.client,requires=IS_IPV4()),
                           Field('Scan_Type', required=True, requires=IS_IN_SET(['NMAP','CSV','NESSUS'], zero=T("Select Scan Type"), error_message=T('Not a valid option. Please see documentation.'))),
                           Field('Task_ID', 'string'),
                           Field('Approver', 'string'),
                           Field('Description','text'),
                           Field('Scanner_IP','string',requires=IS_IPV4()),
                           Field('Justification','text',required=True, requires=IS_NOT_EMPTY()),
                           Field('Results_File','upload',uploadfolder="/tmp",authorize="upload",required=True),
                           submit_button='Import'
                          )
    if form.process().accepted:
        response.flash = T('Import is being processed! Hold tight.')
        if not form.vars.Scan_Type in ['NMAP','CSV','NESSUS']:
            print("Import Results: Critical: Invalid scan type received!!!")
        else:
            pass            
    elif form.errors:
        response.flash = T('form has errors %s' % error_message)
    else:
        response.flash = T('Please fill out the required information.')
    return dict(form=form)