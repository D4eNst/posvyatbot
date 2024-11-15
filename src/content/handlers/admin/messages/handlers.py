from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from content.handlers.admin.messages import ikb
from repository.models import Message
from .states import AdminAddMessageState
from repository.crud.messages import MessageRepo

router = Router()


@router.callback_query(StateFilter(None), F.data.startswith("admin_messages"))
async def admin_messages_list(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    await callback_query.answer()

    # getting page from callback data like "admin_messages page_1"
    page = int(callback_query.data.split()[1].split("_")[1])
    page_size = 5

    cnt, messages = await MessageRepo(session).get_page(page_size, page)
    page_cnt = (cnt - 1) // page_size + 1
    try:
        await callback_query.message.edit_text(
            "Список",
            reply_markup=ikb.admin_messages_ikb(messages, page, page_cnt)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(StateFilter(None), F.data.startswith("admin_add_message"))
async def admin_add_message(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminAddMessageState.GET_MESSAGE_NAME)
    await callback_query.message.edit_text("Введите название:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddMessageState.GET_MESSAGE_NAME, F.text)
async def set_message_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(AdminAddMessageState.GET_MESSAGE_SLUG)
    await message.answer("Введите slug:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddMessageState.GET_MESSAGE_NAME)
async def incorrect_message_name(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите название снова:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddMessageState.GET_MESSAGE_SLUG, F.text)
async def set_message_slug(message: types.Message, state: FSMContext) -> None:
    await state.update_data(slug=message.text)
    await state.set_state(AdminAddMessageState.GET_MESSAGE_TEXT)
    await message.answer("Введите текст сообщения, который увидят участники:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddMessageState.GET_MESSAGE_SLUG)
async def incorrect_message_slug(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите slug снова:", reply_markup=ikb.admin_back_ikb())


@router.message(AdminAddMessageState.GET_MESSAGE_TEXT, F.text)
async def set_message_text(msg: types.Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(text=msg.text)
    data = await state.get_data()
    message_repo = MessageRepo(session)

    try:
        message = await message_repo.create(**data)
        await msg.answer(f"Сохранение сообщения \"{message.name}\" ...")
    except Exception as e:
        await msg.answer(f"Во время создания произошла ошибка: \n{e}")

    await state.clear()
    cnt, messages = await message_repo.get_page(5, 1)
    page_cnt = (cnt - 1) // 5 + 1
    await msg.answer("Список", reply_markup=ikb.admin_messages_ikb(messages, 1, page_cnt))


@router.message(AdminAddMessageState.GET_MESSAGE_TEXT)
async def incorrect_message_text(message: types.Message) -> None:
    await message.answer("Произошла ошибка, введите текст снова:", reply_markup=ikb.admin_back_ikb())


@router.callback_query(StateFilter(None), F.data.startswith("admin_message"))
async def admin_message_info(callback_query: types.CallbackQuery, session: AsyncSession) -> None:
    try:
        message = await MessageRepo(session).get(Message.id == int(callback_query.data.split()[1]))
    except NoResultFound:
        await callback_query.answer(text=f"Ошибка: не найдено", show_alert=True)
        return

    await callback_query.message.edit_text(
        f"<b>Название</b>: {message.name}\n"
        f"<b>Slug</b>: {message.slug}\n"
        f"<b>Текст сообщения</b>: {message.text}",
        reply_markup=ikb.admin_edit_message_ikb(message, current_page=int(callback_query.data.split()[2]))
    )


@router.callback_query(StateFilter(None), F.data.startswith("admin_delete_message"))
async def admin_message_delete(callback_query: types.CallbackQuery, session: AsyncSession) -> None:
    message_repo = MessageRepo(session)

    try:
        await message_repo.delete(Message.id == int(callback_query.data.split()[1]))
        await callback_query.answer("Удаление...")
    except Exception as e:
        await callback_query.answer(f"Ошибка: {e}", show_alert=True)

    cnt, messages = await message_repo.get_page(5, 1)
    page_cnt = (cnt - 1) // 5 + 1
    await callback_query.message.edit_text("Список",
                                           reply_markup=ikb.admin_messages_ikb(messages, 1, page_cnt))
