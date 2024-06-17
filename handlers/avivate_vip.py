import asyncio
from aiogram import F, Router, types, Bot
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.list_users import get_botlang, add_to_list_users_id_message, add_user_vip_list
from database.orm_query import update_user_phonenumber, update_user_bonuses
from filters.chat_types import ChatTypesFilter, OnStateChanges, my_vip_state_list_id_add, my_vip_state_list_id_remove
from kb.keyboard import messages_activate_vip, keyboard_vip_activate, create_contact_request_keyboard, vip_activate_kb, \
    create_keyboard, menu_callback_kb, create_contact_request_keyboard_cancel

activate_vip_router = Router()
activate_vip_router.message.filter(ChatTypesFilter(['private']))
# Определение состояний


@activate_vip_router.message(StateFilter('*'), (F.text == "Отказаться от VIP 🫤") | (F.text == "Refuse VIP 🫤") | (F.text == "VIP-тен бас тарту 🫤"))
async def cancel(message: types.Message, state: FSMContext):
    botlang = await get_botlang()
    current_state = await state.get_state()
    if current_state is None:
        return
    data = await state.get_data()
    chat_ids = data.get('chat_id', [])
    await state.clear()
    await message.answer(f'{await menu_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'menu_kb', 2, 2, 2,
                                                      2).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    chat_ids.append(message.message_id)
    chat_ids.append(message.message_id + 1)
    await add_to_list_users_id_message(message.chat.id, chat_ids)


class VIPState(StatesGroup):
    phone_shared = State()
    bonus_chosen = State()
    vip_activated = State()


@activate_vip_router.message((F.text.lower() == '❌ vip не активен') | (F.text.lower() == '❌ vip is not active') | (F.text.lower() == '❌ vip белсендірілмеген'))#(F.text.lower() == '💵 депозит') | (F.text.lower() == '💵 depozit') | (F.text.lower() == '💵 depósito') |
async def vip(message: types.Message, state: FSMContext):
    botlang = await get_botlang()
    await message.answer(f'{await vip_activate_kb(botlang[message.from_user.id])}',
                         reply_markup=create_contact_request_keyboard(botlang[message.from_user.id]))
    await my_vip_state_list_id_add(message.from_user.id)
    await state.update_data(phone_shared=False, bonus_chosen=False, chosen_bonus=None, chat_id=[message.message_id, message.message_id+1])
    await state.set_state(VIPState.phone_shared)


@activate_vip_router.message(StateFilter(VIPState.phone_shared), F.content_type == ContentType.CONTACT)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    botlang = await get_botlang()
    user_lang = botlang[message.from_user.id]
    await message.answer(messages_activate_vip[user_lang]['thanks_for_phone'], reply_markup=create_contact_request_keyboard_cancel(user_lang))
    data = await state.get_data()
    chat_ids = data.get('chat_id', [])
    chat_ids.append(chat_ids[1]+1)
    chat_ids.append(chat_ids[2]+2)
    chat_ids.append(message.message_id)
    chat_ids.append(message.message_id+1)
    await state.update_data(phone_shared=True, contact=contact, chat_id=chat_ids)
    await message.answer(messages_activate_vip[user_lang]['choose_option'], reply_markup=await keyboard_vip_activate(user_lang))

@activate_vip_router.callback_query(StateFilter(VIPState.phone_shared), F.data.in_(['bonus_casino', 'bonus_sport']))
async def process_bonus(callback_query: CallbackQuery, state: FSMContext):
    botlang = await get_botlang()
    user_lang = botlang[callback_query.from_user.id]
    chosen_bonus = callback_query.data

    await callback_query.answer(messages_activate_vip[user_lang]['bonus_chosen'], show_alert=True)  # Показываем уведомление


    # Проверка перед обновлением разметки
    new_markup = await keyboard_vip_activate(user_lang, chosen_bonus)
    await callback_query.message.edit_reply_markup(reply_markup=new_markup)
    data = await state.get_data()
    chat_ids = data.get('chat_id', [])
    chat_ids.append(callback_query.message.message_id)
    await state.update_data(bonus_chosen=True, chosen_bonus=chosen_bonus, chat_id=chat_ids)

@activate_vip_router.callback_query(StateFilter(VIPState.phone_shared), F.data == 'activate_vip')
async def process_activate_vip(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    botlang = await get_botlang()
    user_lang = botlang[callback_query.from_user.id]
    data = await state.get_data()
    print(data)
    if not data.get('phone_shared') or not data.get('bonus_chosen'):
        await callback_query.answer(messages_activate_vip[user_lang]['complete_all_steps'], show_alert=True)  # Показываем уведомление
    else:
        await callback_query.answer(messages_activate_vip[user_lang]['vip_activated'], show_alert=True)  # Показываем уведомление
        await update_user_phonenumber(session, callback_query.from_user.id, data['contact'].phone_number)
        await update_user_bonuses(session, callback_query.from_user.id, data['chosen_bonus'])
        chat_ids = data['chat_id']
        await state.clear()
        await add_user_vip_list(callback_query.from_user.id)
        await my_vip_state_list_id_remove(callback_query.from_user.id)
        await asyncio.sleep(1)
        await callback_query.message.answer(f'{await menu_callback_kb(user_lang)}',
                                            reply_markup=create_keyboard(user_lang, 'menu_kb', 2, 2, 2, 2).as_markup(
                                                resize_keyboard=True,
                                                input_field_placeholder='Welcome!'))
        chat_ids.append(callback_query.message.message_id + 1)
        await add_to_list_users_id_message(callback_query.message.chat.id, chat_ids)
