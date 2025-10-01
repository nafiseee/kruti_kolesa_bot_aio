client_work_keys = ['work_type', 'full_name', 'phone_number', 'act_id', 'b_model', 'b_id', 'iot_id']
client_work = ['', '', 'Номер телефона: ', 'Акт №', 'Модель велосипеда: ', 'Номер велосипеда: ', 'IoT: ']
async def info(state):

    data = await state.get_data()

    s = f"<b>Мастер:</b> {data['employer_name']} | {data['start_time']}\n\n"
    for q,w in enumerate(client_work_keys):
        if w in data:
            if client_work[q]:
                s+=f"<b>{client_work[q]}</b> {data[w]}\n"
            else:
                s+=f"<b>{data[w]}\n</b>"
    s+='\n<b>Выполненные работы:</b>\n'
    if data['works']==[]:
        for i in range(3):
            s+='____________\n'
    else:
        n = 1
        for i in data['works']:
            if i not in data['works_count']:
                if n<10:
                    s+=" "
                s+=f"{n}| {i}\n"

            else:
                if data['works_count'][i]==1:
                    s += f"{i}\n"
                else:
                    s += f"{i} ({data['works_count'][i]}x)\n"
            n+=1
    s+="\n<b>Запчасти:</b>\n"
    if data['spares']==[]:
        for i in range(3):
            s+='____________\n'
        else:
            for i in data['spares']:
                if i not in data['works_count']:
                    s += f"{i}\n"
                else:
                    if data['works_count'][i] == 1:
                        s += f"{i}\n"
                    else:
                        s += f"{i} ({data['works_count'][i]}x)\n"

    else:
        print(data['spares_types'])
        for i in range(len(data['spares'])):
            if data['spares_types'][i]=='Новый':
                if i+1<10:
                    s+=" "
                s += f"{i + 1}| {data['spares'][i]}\n"

            else:
                s += f"{i + 1}| {data['spares'][i]} [б/у]\n"
            print(data['spares_types'])
    s+=f"\n<b>Норма часы:</b> {round(sum(data['norm_time']),1)}👺"


    # s+='<blockquote>'
    # for i in data.keys():
    #     if i not in ['works','spares','spares_variant']:
    #
    #         s+=str(i)+"   "+str(data[i])
    #         s+="\n"
    # s+="*"*30
    # s+="\nworks:\n"
    # for i in data['works']:
    #     s+=f"{i}\n"
    # s+="spares:\n"
    # for i in data['spares']:
    #     s+=f"{i}\n"
    # s+='</blockquote>'
    # print(s)
    return s


async def info_all_times(a):
    s = "<b>Норма часы за [просто весь период пусть будет]:</b>\n"
    for i in a:
        s+=f"{i}: {a[i]}\n"
    print(s)
    return s