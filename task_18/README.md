§Napište dotaz, který vypíše filmy pro děti od června roku 2020

      CREATE TABLE tvprogram (
        program_date timestamp NOT NULL,
        content_id int NOT NULL,
        channel TEXT NOT NULL,
        PRIMARY KEY(program_date, content_id)
      );
      
      CREATE TABLE content (
        content_id serial PRIMARY KEY,
        title TEXT NOT NULL,
        kids_content TEXT NOT NULL,
        content_Type TEXT NOT NULL
      );
      
      INSERT INTO tvprogram (program_date, content_id, channel) VALUES
      ('2020-06-10 08:00', 1, 'LC-Channel'),
      ('2020-05-11 12:00', 2, 'LC-Channel'),
      ('2020-05-12 12:00', 3, 'LC-Channel'),
      ('2020-05-13 14:00', 4, 'Disney Ch'),
      ('2020-06-18 14:00', 4, 'Disney Ch'),
      ('2020-07-15 16:00', 5, 'Disney Ch');
      
      INSERT INTO content (title, kids_content, content_type) VALUES
      ('Lost in space', 'N', 'Movies'),
      ('Alg. for Kids', 'Y', 'Series'),
      ('Database Sols', 'N', 'Series'),
      ('Aladdin', 'Y', 'Movies'),
      ('Cinderella', 'Y', 'Movies');
      
      Řešení 1
      
      SELECT DISTINCT c.title from tvprogram t 
      LEFT JOIN content c
      USING(content_id)
      WHERE TO_CHAR(program_date,'yyyy-mm')='2020-06'
      AND Kids_content = 'Y'
      AND content_type = 'Movies';
