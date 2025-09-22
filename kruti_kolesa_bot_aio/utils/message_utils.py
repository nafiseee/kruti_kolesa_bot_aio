async def delete_message(message,state):
    data = await state.get_data()
    if 'last_message' in data:
        print(f"Удаление{data['last_message'].text}")
        data['last_message'].delete()

    data['last_message']=message
    await state.update_data(data)
