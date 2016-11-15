#!/usr/bin/python

import os
from dateutil import parser

class getaxodelObject(object):
    def __init__(self,events=None,secuentialCodeChunks=None):
        for x in events:
            self.addEvent(x)

class getaxodelEvent(object):

    pass

class getaxodelNonSequentialCodeChunk(object):

    pass

    # a set of rules or conditions
    
class getaxodelSecuentialCodeChunk(object):

    pass

    # a secuentialCodeChunk can be:
    # the main part of a getaxodelObject
    # a subroutine
    # an event

class getaxodelDeclarativeDataDescription(object):

    ddd=[]

    def __init__(self,identifier=None,datatype=None):
        self.addElement(identifier=identifier,datatype=datatype)
    def addElement(self,identifier=None,datatype=None):
        g=getaxodelDataElement
        self.ddd.append(g(identifier=identifier,datatype=datatype))

    # A Data Description is a LIST of data elements 
    # or -as a hierarchy- other Data Descriptions.
    # The order in the list is very important,
    # data elements are annotated with
    #    an identifier
    #    whether it is a primary key ={True, False}
    #    its data type

class getaxodelDataElement(object):
    
    def __init__(self,identifier=None,datatype=None):
        self.identifier=identifier
        self.datatype=datatype

fn='text.xpw'
f=open(fn,'r', encoding='latin1')
stack=[]
n=0
joinedtags={}
WorkPanelFormBlockTextSource='/'.join(['WorkPanel', 'Form', 'Block', 'Text', 'Source'])
ReportLayoutBlockTextSource='/'.join(['Report', 'Layout', 'Block', 'Text', 'Source'])
TransactionFormBlockTextSource='/'.join(['Transaction', 'Form', 'Block', 'Text', 'Source'])
ProcedureLayoutBlockTextSource='/'.join(['Procedure', 'Layout', 'Block', 'Text', 'Source'])
jt=''
levelUp=False
levelDown=False
tables_and_keys={}
for x in f.readlines():
    x=x[0:-1]
    n+=1
    if jt == WorkPanelFormBlockTextSource or \
       jt == ReportLayoutBlockTextSource or \
       jt == TransactionFormBlockTextSource or \
       jt == ProcedureLayoutBlockTextSource:
        xstrip=x.strip()
        if xstrip == ':eSource':
            gx_object_contents.append(x)
            stack.pop()
            levelDown=True
            jt='/'.join(stack)
            continue
    else:
        try:
            # Ubicación léxica de una línea de tag.
            xstrip=x.strip()
            i=xstrip.index(':')
            if i==0:
                if xstrip[1]!='e':
                    
                    # Inicio de tag (":Tag"), actualizar el stack, actualizar la stack string jt, eventos relativos a apertura de tag.
                    tag=xstrip[1:]
                    stack.append(tag)
                    levelUp=True
                    jt='/'.join(stack)

                    # Carga de estructura de datos de la estadística de la jerarquía de tags en el archivo xpw.
                    try:
                        joinedtags[jt][1]+=1
                    except:
                        joinedtags[jt]=[n,1]

                    is_fileable_object=stack[0] in "WorkPanel Report Transaction Procedure".split()
                    if len(stack)==1:
                        # Inicialización para main
                        is_main_gx_object = ""

                        # Inicialización de nombre de objeto gx
                        collected_filename = None
                        collected_object_type=stack[0]

                        # Inicialización de fecha y hora del objeto
                        gx_object_datetime = None
                        
                        # Inicialización de contenido del tag cabecera del xpw
                        if stack[0]=='KMW':
                            gx_KMW_tag_contents = []
                        
                        # Inicialización de contenido de objeto gx
                        gx_object_contents = []

                else:
                    
                    # Recordar tag cabecera del xpw (última línea de la cabecera)
                    if len(stack)==1:
                        if stack[0]=='KMW':
                            try:
                                gx_KMW_tag_contents.append(x)
                            except:
                                pass

                    
                    # Finalización de tag (":eTag"), actualizar el stack, actualizar la stack string jt, eventos relativos a cierre de tag genérico o específico.
                    tag=xstrip[2:]
                    stack.pop()
                    jt='/'.join(stack)

                    # Recordar contenido de objeto gx
                    try:
                        gx_object_contents.append(x)
                    except NameError:
                        pass

                    # Carga de estructura de datos relativa a tablas e índices de la base de conocimiento.
                    if jt=='/'.join(['Table']):
                        try:
                            tables_and_keys[current_table]['indices'].append(index)
                        except:
                            tables_and_keys[current_table]['indices'].append(None)

                    # Grabar archivo con el contenido del Tag principal cerrado, si hay nombre de archivo relevado para asignar.
                    if len(stack)==0:
                        try:
                            ot={'Procedure':'P','WorkPanel':'W','Report':'R','Transaction':'T'}[collected_object_type]
                            file_to_write=open("repogx1/%s%s.gxObj"%(ot,collected_filename),'w',encoding='latin1')

                            file_to_write.write( "\r\n".join(gx_KMW_tag_contents+gx_object_contents))
                            file_to_write.close()
                            if gx_object_datetime:
                                print(gx_object_datetime)
                                print(gx_object_datetime.timestamp())
                                os.utime("repogx1/%s%s.gxObj"%(ot,collected_filename),times=(gx_object_datetime.timestamp(),gx_object_datetime.timestamp()))
                        except NameError:
                            pass
                        except KeyError:
                            pass

                    continue



        except ValueError:
            pass



    jt='/'.join(stack)

    if jt=='/'.join(['Table']):
        #print(xstrip)
        if levelUp:
            pk=[]
        if xstrip.startswith('Key='):
            pk.append(xstrip[4:])

    if jt=='/'.join(['Table','Info']) :
        #print(xstrip)
        if xstrip.startswith('Name='):
            current_table=xstrip[5:]
            tables_and_keys[current_table]={}
            tables_and_keys[current_table]['pk']=pk
            tables_and_keys[current_table]['indices']=[]

    if jt=='/'.join(['Table','TblIndex']):
        if levelUp:
            index=[]

    if jt=='/'.join(['Table','TblIndex','IdxAttri']):
        if xstrip.startswith('Name='):
            index.append(xstrip[5:])
            
    # Análisis de nombre
            
    if len(stack)==2 and stack[1]=='Info':
        if  x.startswith('    Name='):
            collected_filename=x[x.index("=")+1:]
        

    # Análisis de objeto gx "main"
            
    if len(stack)==2 and stack[1]=="ObjInfo":
        is_main_gx_object = " || ".join([is_main_gx_object,x])
        print(is_main_gx_object)


    # Recordar tag cabecera del xpw
    if len(stack)==1:
        if stack[0]=='KMW':
            try:
                gx_KMW_tag_contents.append(x)
            except:
                pass
        if stack[0] in "WorkPanel Report Transaction Procedure".split():
            if  x.startswith('  LastUpdate=') and not gx_object_datetime:
                try:
                    gx_object_datetime=parser.parse(x[x.index('=')+1:])
                    
                except:
                    gx_object_datetime=parser.parse("1980-01-01 00:00:00")
    
    # Recordar contenido de objeto gx
    try:
        gx_object_contents.append(x)
    except NameError:
        pass

    levelUp=False
    levelDown=False

