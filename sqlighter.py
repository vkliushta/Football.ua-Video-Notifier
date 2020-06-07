import sqlite3

class SQLighter:

    def __init__(self, database_file):
        '''Connect to our database'''
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        '''Get all active subscribers'''
        with self.connection:
            return self.cursor.execute('SELECT * FROM `subscriptions` WHERE `status` = ?', (status,)).fetchall()
    
    def subscriber_exists(self, user_id):
        '''Return is subscriber in our database or not'''
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status):
        '''Add subscriber'''
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES (?,?)", (user_id, status))
    
    def update_subscription(self, user_id, status):
        '''Update subscriber status'''
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def last_video(self, id_ = 1):
        '''Return last video'''
        with self.connection:
            return self.cursor.execute('SELECT `video` FROM `last_video` WHERE `id` = ?', (id_,)).fetchall()

    def update_video(self, video, id_ = 1):
        '''Update last video'''
        with self.connection:
            return self.cursor.execute("UPDATE `last_video` SET `video` = ? WHERE `id` = ?", (video, id_))

    def close(self):
        '''Close connection with database'''
        self.connection.close()