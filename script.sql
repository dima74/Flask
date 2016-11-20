DROP TABLE if EXISTS Messages;
DROP TABLE if EXISTS FileLinks;
DROP TABLE if EXISTS ChatToUsers;
DROP TABLE if EXISTS UserNames;
DROP TABLE if EXISTS ChatNames;

CREATE TABLE Messages (messageId INT, chatId INT, userId INT, content TEXT);
CREATE TABLE FileLinks (messageId INT, type INT, path TEXT, name TEXT);
CREATE TABLE ChatsToUsers (chatId INT, userId INT);
CREATE TABLE UserNames (userId INT, name TEXT);
CREATE TABLE ChatNames (chatId INT, name TEXT);

insert into Messages values(1, 1, 1, 'test');
insert into Messages values(2, 1, 2, 'another');
insert into Messages values(3, 1, 3, 'another');
insert into Messages values(4, 2, 2, 'hello');

insert into FileLinks values(1, 1, '1.txt', '1');
insert into FileLinks values(2, 2, '2.txt', '2');
insert into FileLinks values(3, 3, '3.txt', '3');
insert into FileLinks values(1, 4, '4.txt', '4');
insert into FileLinks values(1, 5, '5.txt', '5');

insert into ChatNames values(1, 'chat1');
insert into ChatNames values(2, 'chat2');
insert into ChatNames values(3, 'chat3');

insert into ChatsToUsers values(1, 1);
insert into ChatsToUsers values(1, 2);
insert into ChatsToUsers values(2, 1);

insert into UserNames values(1, 'user1');
insert into UserNames values(2, 'user2');
insert into UserNames values(3, 'user3');

select * from Messages;
select * from ChatNames;
select * from UserNames;

/*SELECT Messages.messageId, Messages.chatId, Messages.userId, Messages.content, UserNames.name, ChatNames.name
FROM Messages, UserNames, ChatNames
WHERE Messages.chatId = ChatNames.chatId AND Messages.userId = UserNames.userId AND Messages.chatId = 1;

SELECT type, path, name
FROM FileLinks
WHERE messageId = 1;*/

/*SELECT Messages.messageId, *//*Messages.chatId, Messages.userId, *//*Messages.content, UserNames.name, ChatNames.name, FileLinks.type, FileLinks.path, FileLinks.name
FROM Messages, UserNames, ChatNames, FileLinks
WHERE Messages.chatId = ChatNames.chatId AND Messages.userId = UserNames.userId AND Messages.messageId = FileLinks.messageId AND Messages.chatId = 1
GROUP BY Messages.messageId;*/

SELECT * FROM ChatNames;
SELECT * FROM ChatsToUsers;
SELECT ChatNames.chatId, ChatNames.name FROM ChatsToUsers, ChatNames WHERE ChatNames.chatId = ChatsToUsers.chatId and ChatsToUsers.userId = 1;
