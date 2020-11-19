-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 18 Kas 2020, 19:53:45
-- Sunucu sürümü: 10.4.14-MariaDB
-- PHP Sürümü: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `usblog`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `content` text NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `content`, `created_date`) VALUES
(4, 'İkarus Creative | Tüm Hakları Saklıdır.', 'ugursemizoglu', '<p><img alt=\"\" src=\"https://www.ikaruscreative.com/wp-content/themes/ikaruscreative/assets/img/logo/ikarus.png\" style=\"height:87px; width:192px\" /></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><em>Uğur</em> <em><strong>SEMİZOĞLU</strong></em><br />\r\n<em>Web Yazılım ve Tasarımcısı</em><br />\r\n<strong>Tel :</strong> <em>0561 619 16 01</em></p>\r\n', '2020-11-16 20:43:27'),
(5, 'Deneme Ürün 4', 'ugursemizoglu', '<p>Deneme &Uuml;r&uuml;n 4</p>\r\n', '2020-11-18 18:38:47'),
(6, 'Deneme Kod', 'ugursemizoglu', '<p>Deneme Kod :</p>\r\n\r\n<p>&nbsp;</p>\r\n<pre class=\"prettyprint\">class Voila {\r\npublic:\r\n  // Voila\r\n  static const string VOILA = \"Voila\";\r\n\r\n  // will not interfere with embedded <a href=\"#voila2\">tags</a>.\r\n}</pre>', '2020-11-18 18:48:33');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(1, 'Uğur Semizoğlu', 'ugursemizoglu54@gmail.com', 'usemizoglu', '$5$rounds=535000$/DCrlxJyglZu8jkt$2KGsq8NMzuPfDc0GgYkmHzKMqIJt74gxfpE2KUSZLy8'),
(3, 'Melike Semizoğlu', 'melike.gook@gmail.com', 'melikesemizoglu', '$5$rounds=535000$/tDV4zblMzT2Wg2t$AIMjPdum2YUS34lzD9oWPhn4r8aaPfzXSDhy0/L3axC'),
(4, 'Ugur Semizoglu', 'ugursemizoglu54@gmail.com', 'ugursemizoglu', '$5$rounds=535000$kkNzrPuCr2q.bDxo$47maJZkJadT02Dq2OGFx2NgqVcuKWHPZIoY71Rho0D7');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
