-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Мар 29 2025 г., 19:40
-- Версия сервера: 10.11.8-MariaDB-0ubuntu0.24.04.1
-- Версия PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `vpn_bot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `checks`
--

CREATE TABLE `checks` (
  `id` int(11) NOT NULL,
  `check_id` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `status` text NOT NULL,
  `date` timestamp NOT NULL,
  `server_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `checks`
--

INSERT INTO `checks` (`id`, `check_id`, `user_id`, `amount`, `status`, `date`, `server_date`) VALUES
(3, '2f791292-000f-5000-a000-1e1dad1577ab', 1324016724, 3, 'pending', '2025-03-28 16:56:02', '2025-03-27 00:14:21'),
(4, '2f79c406-000f-5000-8000-16d5b4fd062a', 1324016724, 3, 'succeeded', '2025-03-29 07:33:10', '2025-03-29 09:34:14'),
(5, '2f79c494-000f-5000-b000-13d94d2f5039', 1324016724, 3, 'pending', '2025-03-29 07:35:32', '2025-03-29 09:35:59');

-- --------------------------------------------------------

--
-- Структура таблицы `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `type` text DEFAULT NULL,
  `text` text DEFAULT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `logs`
--

INSERT INTO `logs` (`id`, `type`, `text`, `date`) VALUES
(49, 'Balance_Add', '1324016724, Money 0 + 100 = 200', '2025-03-29 09:50:43'),
(50, 'NewDayMinusMoney', 'user_id: 1324016724, Money 100 - 3 = 97', '2025-03-29 20:12:01');

-- --------------------------------------------------------

--
-- Структура таблицы `settings`
--

CREATE TABLE `settings` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `tariffDay` int(11) NOT NULL DEFAULT 3,
  `domain` text NOT NULL,
  `XPay` float NOT NULL DEFAULT 1,
  `StartingBalance` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `settings`
--

INSERT INTO `settings` (`id`, `date`, `tariffDay`, `domain`, `XPay`, `StartingBalance`) VALUES
(0, '2025-03-28', 3, 'https://fin-01.kadtale.site', 1, 15);

-- --------------------------------------------------------

--
-- Структура таблицы `text`
--

CREATE TABLE `text` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `text` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `text`
--

INSERT INTO `text` (`id`, `name`, `text`) VALUES
(1, 'info_vpn_command_text', '⚫🔴 RoZkomVPN 🛡️️\\n\\n\\n🔹 Мгновенный и удобный VPN прямо в Telegram\\n\\n\\n✅ Доступ к Instagram, YouTube, TikTok и др.\\n\\n\\n🚀 Высокая скорость\\n\\n\\n🛜 Стабильное соединение\\n\\n\\n💳 Оплата картами РФ и СБП\\n\\n\\n⚡️ Шифрование трафика и скрытие IP\\n\\n\\n💸 1 День пользования - '),
(2, 'buy_subscription_command_text', 'Введите сумму для пополнения\\n1 месяц - 93₽ (3₽/день)\\n\\nАкции:\\n3 месяца - 279₽\\n6 месяцев - 558₽\\n12 месяцев - 1116₽\\n\\n⬇️ Введите сумму для пополнения ⬇️'),
(3, 'help_command_text', 'Меню помощи:\\n\\nВ случае если вы не нашли ответ на вопрос здесь, можете написать в нашу поддержку, которая вам с радостью поможет!'),
(4, 'payment_problems_text', 'В редких случаях платеж может обрабатываться до 24 часов.\\n\\nЕсли деньги не поступили, пожалуйста, свяжитесь с нами.'),
(5, 'low_speed_problems', 'Для совершенствования качества предоставляемых услуг,\\nпросим вас указать следующую информацию:\\n1. Тип вашего устройства.\\n2. Используемое приложение для подключения к VPN.\\n3. Приблизительное время возникновения задержек.\\n4. Приложение или веб-сайт, где наблюдаются задержки.\\n\\n (Указывать все это в поддержке)'),
(6, 'vpn_no_work', 'Если возникают проблемы с работой VPN, попробуйте следующее:\\n\\n1) Проверьте состояние баланса.\\n2) Обновите приложение, если это необходимо.\\n3) Перезагрузите устройство.\\n4) Убедитесь, что в настройках не активированы другие VPN-сервисы.\\n\\nЕсли ни один из этих способов не решает проблему, пожалуйста, свяжитесь с оператором, нажав на кнопку ниже.');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `balance` int(11) NOT NULL,
  `admin_status` int(11) DEFAULT 0,
  `functin_status` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`user_id`, `balance`, `admin_status`, `functin_status`) VALUES
(1324016724, 97, 1, NULL),
(1785293901, 15, 0, NULL);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `checks`
--
ALTER TABLE `checks`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `text`
--
ALTER TABLE `text`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `checks`
--
ALTER TABLE `checks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT для таблицы `settings`
--
ALTER TABLE `settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `text`
--
ALTER TABLE `text`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1785293902;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
