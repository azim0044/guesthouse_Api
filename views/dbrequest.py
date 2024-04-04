from datetime import timedelta
import datetime
import json
import shortuuid

class DatabaseRequest:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_detail(self, query_type, data):
        cur = self.mysql.connection.cursor()

        if query_type == 'LOGIN_USER':
            userEmail = data[0]

            sql_query = """
                SELECT userId, userEmail, userPassword, 'user' as userType FROM users WHERE userEmail = %s
                UNION
                SELECT adminId as userId, adminEmail as userEmail, adminPassword as userPassword, 'admin' as userType FROM admin WHERE adminEmail = %s
            """

            cur.execute(sql_query, (userEmail, userEmail))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'CHECK_USER':
            userEmail = data[0]

            sql_query = """
               SELECT * FROM users WHERE userEmail = %s 
            """

            cur.execute(sql_query, (userEmail,))
            result = cur.fetchone()
            cur.close()
            return result
        
        if query_type == 'GET_USER':
            userId = data[0]

            sql_query = """
               SELECT * FROM users WHERE userId = %s 
            """

            cur.execute(sql_query, (userId,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_ALL_USER':

            sql_query = """
               SELECT * FROM users;
            """

            cur.execute(sql_query)
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = [dict(zip(column_names, row)) for row in result] if column_names and result else []
            cur.close()
            return result_dict
        
        if query_type == 'GET_HOUSES':
            book_from = data[0]
            book_to = data[1]
            result_dict = []
    
            cur.execute("""
                SELECT
                    h.houseId AS id,
                    h.houseName,
                    h.houseCategory,
                    h.houseDescription,
                    h.houseThumbnail,
                    h.houseBed,
                    h.housePeople,
                    h.housePrice,
                    h.houseStatus,
                    h.houseAvailability,
                    hl.houseLocation,
                    hl.houseAddress,
                    AVG(ur.rate) AS ratingScore,
                    COUNT(ur.reviewId) AS totalReview
                FROM
                    house h
                LEFT JOIN
                    houselocation hl ON h.houseId = hl.houseId
                LEFT JOIN
                    userreview ur ON h.houseId = ur.houseId
                LEFT JOIN
                    reservation r ON h.houseId = r.houseId
                WHERE
                    (r.bookStartDate IS NULL OR r.bookEndDate IS NULL) -- Exclude houses with any reservations
                    OR (
                        (r.bookStartDate > %s OR r.bookEndDate < %s) -- Exclude reservations completely outside the desired range
                        AND (r.bookStartDate < %s OR r.bookEndDate > %s) -- Exclude reservations completely outside the desired range
                    )
                    AND r.bookHouseStatus != 'Check-Out'
                GROUP BY
                    h.houseId
            """, (book_to, book_from, book_to, book_from))

            house_data = cur.fetchall()
            house_column_names = [desc[0] for desc in cur.description] if cur.description else []
            
            # Fetch house images
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', images, '"') SEPARATOR ','), ']') AS houseImages
                FROM
                    houseimages
                GROUP BY
                    houseId
            """)
            house_images_data = cur.fetchall()
            house_images_dict = {row[0]: json.loads(row[1]) for row in house_images_data}
            
            # Fetch house facilities
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', facName, '"') SEPARATOR ','), ']') AS houseFacility
                FROM
                    housefacilities
                GROUP BY
                    houseId
            """)
            house_facilities_data = cur.fetchall()
            house_facilities_dict = {row[0]: json.loads(row[1]) for row in house_facilities_data}
            
            
            # Fetch user reviews
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(
                        JSON_OBJECT(
                            'profileImage', userImage,
                            'userName', userFullName,
                            'reviewNote', reviewNote,
                            'rate', rate
                        ) SEPARATOR ','
                    ), ']') AS userReview
                FROM
                    userreview
                JOIN
                    users ON userreview.userId = users.userId
                GROUP BY
                    houseId
            """)
            user_reviews_data = cur.fetchall()
            user_reviews_dict = {row[0]: json.loads(row[1]) for row in user_reviews_data}
            
            # Combine data into the desired format
            for row in house_data:
                house_id = row[0]
                house_dict = {
                    'id': str(row[0]),
                    'houseName': row[1],
                    'houseCategory': row[2],
                    'houseDescription': row[3],
                    'houseThumbnail': row[4],
                    'houseBed': str(row[5]),
                    'housePeople': str(row[6]),
                    'housePrice': '{:.2f}'.format(row[7]),
                    'houseStatus': row[8],
                    'houseAvailability': row[9],
                    'houseLocation': row[10],
                    'houseAddress': row[11],
                    'ratingScore': '{:.2f}'.format(row[12]) if row[12] is not None else None,
                    'totalReview': str(row[13]),
                    'houseImages': house_images_dict.get(house_id, []),
                    'houseFacility': house_facilities_dict.get(house_id, []),
                    'userReview': user_reviews_dict.get(house_id, [])
                }
                result_dict.append(house_dict)
            
            return result_dict
        
        if query_type == 'ADMIN_ALL_HOUSE':
            result_dict = []
    
            cur.execute("""
                SELECT
                    h.houseId AS id,
                    h.houseName,
                    h.houseCategory,
                    h.houseDescription,
                    h.houseThumbnail,
                    h.houseBed,
                    h.housePeople,
                    h.housePrice,
                    h.houseStatus,
                    h.houseAvailability,
                    hl.houseLocation,
                    hl.houseAddress,
                    AVG(ur.rate) AS ratingScore,
                    COUNT(ur.reviewId) AS totalReview
                FROM
                    house h
                LEFT JOIN
                    houselocation hl ON h.houseId = hl.houseId
                LEFT JOIN
                    userreview ur ON h.houseId = ur.houseId
                LEFT JOIN
                    reservation r ON h.houseId = r.houseId
                GROUP BY
                    h.houseId
            """)

            house_data = cur.fetchall()
            house_column_names = [desc[0] for desc in cur.description] if cur.description else []
            
            # Fetch house images
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', images, '"') SEPARATOR ','), ']') AS houseImages
                FROM
                    houseimages
                GROUP BY
                    houseId
            """)
            house_images_data = cur.fetchall()
            house_images_dict = {row[0]: json.loads(row[1]) for row in house_images_data}
            
            # Fetch house facilities
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', facName, '"') SEPARATOR ','), ']') AS houseFacility
                FROM
                    housefacilities
                GROUP BY
                    houseId
            """)
            house_facilities_data = cur.fetchall()
            house_facilities_dict = {row[0]: json.loads(row[1]) for row in house_facilities_data}
            
            
            # Fetch user reviews
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(
                        JSON_OBJECT(
                            'profileImage', userImage,
                            'userName', userFullName,
                            'reviewNote', reviewNote,
                            'rate', rate
                        ) SEPARATOR ','
                    ), ']') AS userReview
                FROM
                    userreview
                JOIN
                    users ON userreview.userId = users.userId
                GROUP BY
                    houseId
            """)
            user_reviews_data = cur.fetchall()
            user_reviews_dict = {row[0]: json.loads(row[1]) for row in user_reviews_data}
            
            # Combine data into the desired format
            for row in house_data:
                house_id = row[0]
                house_dict = {
                    'id': str(row[0]),
                    'houseName': row[1],
                    'houseCategory': row[2],
                    'houseDescription': row[3],
                    'houseThumbnail': row[4],
                    'houseBed': str(row[5]),
                    'housePeople': str(row[6]),
                    'housePrice': '{:.2f}'.format(row[7]),
                    'houseStatus': row[8],
                    'houseAvailability': row[9],
                    'houseLocation': row[10],
                    'houseAddress': row[11],
                    'ratingScore': '{:.2f}'.format(row[12]) if row[12] is not None else None,
                    'totalReview': str(row[13]),
                    'houseImages': house_images_dict.get(house_id, []),
                    'houseFacility': house_facilities_dict.get(house_id, []),
                    'userReview': user_reviews_dict.get(house_id, [])
                }
                result_dict.append(house_dict)
            
            return result_dict

        if query_type == 'CHECK_FAVOURITE':
            userId = data[0]
            houseId = data[1]

            sql_query = """
               SELECT * FROM userfavourite WHERE userId = %s AND houseId = %s
            """

            cur.execute(sql_query, (userId, houseId,))
            result = cur.fetchone()
            cur.close()
            return result
        
        if query_type == 'GET_FAVOURITE':
            userId = data[0]
            result_dict = []

            cur.execute("""
            SELECT
                h.houseId AS id,
                h.houseName,
                h.houseCategory,
                h.houseDescription,
                h.houseThumbnail,
                h.houseBed,
                h.housePeople,
                h.housePrice,
                h.houseStatus,
                h.houseAvailability,
                hl.houseLocation,
                hl.houseAddress,
                AVG(ur.rate) AS ratingScore,
                COUNT(ur.reviewId) AS totalReview
            FROM
                house h
            LEFT JOIN
                houselocation hl ON h.houseId = hl.houseId
            LEFT JOIN
                userreview ur ON h.houseId = ur.houseId
            LEFT JOIN
                userFavourite uf ON h.houseId = uf.houseId
            WHERE
                uf.houseId IS NOT NULL
                AND uf.userId = %s
            GROUP BY
                h.houseId
        """, (userId,))

            house_data = cur.fetchall()
            house_column_names = [desc[0] for desc in cur.description] if cur.description else []

            # Fetch house images
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', images, '"') SEPARATOR ','), ']') AS houseImages
                FROM
                    houseimages
                GROUP BY
                    houseId
            """)
            house_images_data = cur.fetchall()
            house_images_dict = {row[0]: json.loads(row[1]) for row in house_images_data}

            # Fetch house facilities
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', facName, '"') SEPARATOR ','), ']') AS houseFacility
                FROM
                    housefacilities
                GROUP BY
                    houseId
            """)
            house_facilities_data = cur.fetchall()
            house_facilities_dict = {row[0]: json.loads(row[1]) for row in house_facilities_data}

            # Fetch user reviews
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(
                        JSON_OBJECT(
                            'profileImage', userImage,
                            'userName', userFullName,
                            'reviewNote', reviewNote,
                            'rate', rate
                        ) SEPARATOR ','
                    ), ']') AS userReview
                FROM
                    userreview
                JOIN
                    users ON userreview.userId = users.userId
                GROUP BY
                    houseId
            """)
            user_reviews_data = cur.fetchall()
            user_reviews_dict = {row[0]: json.loads(row[1]) for row in user_reviews_data}

            # Combine data into the desired format
            for row in house_data:
                house_id = row[0]
                house_dict = {
                    'id': str(row[0]),
                    'houseName': row[1],
                    'houseCategory': row[2],
                    'houseDescription': row[3],
                    'houseThumbnail': row[4],
                    'houseBed': str(row[5]),
                    'housePeople': str(row[6]),
                    'housePrice': '{:.2f}'.format(row[7]),
                    'houseStatus': row[8],
                    'houseAvailability': row[9],
                    'houseLocation': row[10],
                    'houseAddress': row[11],
                    'ratingScore': '{:.2f}'.format(row[12]) if row[12] is not None else None,
                    'totalReview': str(row[13]),
                    'houseImages': house_images_dict.get(house_id, []),
                    'houseFacility': house_facilities_dict.get(house_id, []),
                    'userReview': user_reviews_dict.get(house_id, [])
                }
                result_dict.append(house_dict)

            return result_dict
        
        if query_type == 'GET_SELECTED_HOUSE':
            house_id = data[0]
            result_dict = []

            cur.execute("""
                SELECT
                    h.houseId AS id,
                    h.houseName,
                    h.houseCategory,
                    h.houseDescription,
                    h.houseThumbnail,
                    h.houseBed,
                    h.housePeople,
                    h.housePrice,
                    h.houseStatus,
                    h.houseAvailability,
                    hl.houseLocation,
                    hl.houseAddress,
                    AVG(ur.rate) AS ratingScore,
                    COUNT(ur.reviewId) AS totalReview
                FROM
                    house h
                LEFT JOIN
                    houselocation hl ON h.houseId = hl.houseId
                LEFT JOIN
                    userreview ur ON h.houseId = ur.houseId
                WHERE
                    h.houseId = %s
                GROUP BY
                    h.houseId
            """, (house_id,))

            house_data = cur.fetchall()
            house_column_names = [desc[0] for desc in cur.description] if cur.description else []

            # Fetch house images
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', images, '"') SEPARATOR ','), ']') AS houseImages
                FROM
                    houseimages
                WHERE
                    houseId = %s
                GROUP BY
                    houseId
            """, (house_id,))
            house_images_data = cur.fetchall()
            house_images_dict = {row[0]: json.loads(row[1]) for row in house_images_data}

            # Fetch house facilities
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(CONCAT('"', facName, '"') SEPARATOR ','), ']') AS houseFacility
                FROM
                    housefacilities
                WHERE
                    houseId = %s
                GROUP BY
                    houseId
            """, (house_id,))
            house_facilities_data = cur.fetchall()
            house_facilities_dict = {row[0]: json.loads(row[1]) for row in house_facilities_data}

            # Fetch user reviews
            cur.execute("""
                SELECT
                    houseId,
                    CONCAT('[', GROUP_CONCAT(
                        JSON_OBJECT(
                            'profileImage', userImage,
                            'userName', userFullName,
                            'reviewNote', reviewNote,
                            'rate', rate
                        ) SEPARATOR ','
                    ), ']') AS userReview
                FROM
                    userreview
                JOIN
                    users ON userreview.userId = users.userId
                WHERE
                    houseId = %s
                GROUP BY
                    houseId
            """, (house_id,))
            user_reviews_data = cur.fetchall()
            user_reviews_dict = {row[0]: json.loads(row[1]) for row in user_reviews_data}

            # Combine data into the desired format
            for row in house_data:
                house_id = row[0]
                house_dict = {
                    'id': str(row[0]),
                    'houseName': row[1],
                    'houseCategory': row[2],
                    'houseDescription': row[3],
                    'houseThumbnail': row[4],
                    'houseBed': str(row[5]),
                    'housePeople': str(row[6]),
                    'housePrice': '{:.2f}'.format(row[7]),
                    'houseStatus': row[8],
                    'houseAvailability': row[9],
                    'houseLocation': row[10],
                    'houseAddress': row[11],
                    'ratingScore': '{:.2f}'.format(row[12]) if row[12] is not None else None,
                    'totalReview': str(row[13]),
                    'houseImages': house_images_dict.get(house_id, []),
                    'houseFacility': house_facilities_dict.get(house_id, []),
                    'userReview': user_reviews_dict.get(house_id, [])
                }
                result_dict.append(house_dict)

            return result_dict

        if query_type == 'GET_HOUSE_RESERVATION':
            houseId = data[0]
            sql_query = """
            SELECT bookStartDate, bookEndDate FROM reservation WHERE houseId = %s
            """

            cur.execute(sql_query, (houseId,))
            result = cur.fetchall()
            reservation_dates = set()

            for row in result:
                start_date = row[0] 
                end_date = row[1]    

                current_date = start_date
                while current_date <= end_date:
                    reservation_dates.add(current_date.strftime('%Y-%m-%d'))
                    current_date += timedelta(days=1)

            return list(reservation_dates)
                
        if query_type == 'GET_RESERVATION':
            userId = data[0]
            status = data[1].lower() 
            current_date = datetime.datetime.now().date()

            sql_query = """
                SELECT
                    r.reservationId,
                    r.bookStartDate,
                    r.bookEndDate,
                    r.bookStatus,
                    r.totalAmount,
                    r.bookHouseStatus,
                    r.userId,
                    h.houseName,
                    h.houseThumbnail,
                    h.houseId,
                    h.housePrice
                FROM
                    reservation r
                JOIN
                    house h ON r.houseId = h.houseId
                WHERE
                    r.userId = %s
            """

            params = [userId]

            if status in ['pending', 'approved']:
                sql_query += " AND LOWER(r.bookStatus) = %s"  
                params.append(status)
            elif status == 'todaybook': 
                sql_query = """
                    SELECT
                        r.reservationId,
                        r.bookStartDate,
                        r.bookEndDate,
                        CASE
                            WHEN %s BETWEEN r.bookStartDate AND r.bookEndDate THEN "Today's Book"
                            ELSE r.bookStatus
                        END AS bookStatus,
                        r.totalAmount,
                        r.bookHouseStatus,
                        r.userId,
                        h.houseName,
                        h.houseThumbnail,
                        h.houseId,
                        h.housePrice
                    FROM
                        reservation r
                    JOIN
                        house h ON r.houseId = h.houseId
                    WHERE
                        r.userId = %s
                        AND LOWER(r.bookStatus) = 'approved'  # Convert bookStatus to lower case
                        AND %s BETWEEN r.bookStartDate AND r.bookEndDate
                        AND r.bookHouseStatus != 'Check-Out'
                """
                params = [current_date, userId, current_date]

            cur.execute(sql_query, params)
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = [dict(zip(column_names, row)) for row in result] if column_names and result else []
            cur.close()
            return result_dict

        if query_type == 'GET_SERVICE_REQUEST':
            userId = data[0]
            reservationId = data[1]

            sql_query = """
                SELECT * FROM servicerequest WHERE userId = %s AND reservationId = %s
            """

            cur.execute(sql_query, (userId, reservationId,))
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = [dict(zip(column_names, row)) for row in result] if column_names and result else []
            cur.close()
            return result_dict
        
        if query_type == 'GET_HOUSE_POLICY':
            sql_query = """
                SELECT * FROM policy
            """

            cur.execute(sql_query)
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = [dict(zip(column_names, row)) for row in result] if column_names and result else []
            cur.close()
            return result_dict

        if query_type == 'GET_ALL_RESERVATION':
            status = data[0].lower() 
            current_date = datetime.datetime.now().date()

            sql_query = """
                SELECT
                    r.reservationId,
                    r.bookStartDate,
                    r.bookEndDate,
                    r.bookStatus,
                    r.totalAmount,
                    r.bookHouseStatus,
                    r.userId,
                    h.houseName,
                    h.houseThumbnail,
                    h.houseId,
                    h.housePrice
                FROM
                    reservation r
                JOIN
                    house h ON r.houseId = h.houseId
            """

            params = []

            if status in ['pending', 'approved']:
                sql_query += " AND LOWER(r.bookStatus) = %s"  
                params.append(status)
            elif status == 'todaybook': 
                sql_query = """
                    SELECT
                        r.reservationId,
                        r.bookStartDate,
                        r.bookEndDate,
                        r.userId,
                        CASE
                            WHEN %s BETWEEN r.bookStartDate AND r.bookEndDate THEN "Today's Book"
                            ELSE r.bookStatus
                        END AS bookStatus,
                        r.totalAmount,
                        r.bookHouseStatus,
                        h.houseName,
                        h.houseThumbnail,
                        h.houseId,
                        h.housePrice
                    FROM
                        reservation r
                    JOIN
                        house h ON r.houseId = h.houseId
                    WHERE
                        AND LOWER(r.bookStatus) = 'approved'  # Convert bookStatus to lower case
                        AND %s BETWEEN r.bookStartDate AND r.bookEndDate
                        AND r.bookHouseStatus != 'Check-Out'
                """
                params = [current_date, userId, current_date]

            cur.execute(sql_query, params)
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = [dict(zip(column_names, row)) for row in result] if column_names and result else []
            cur.close()
            return result_dict

        if query_type == 'GET_ALL_SERVICE_REQUEST':
            serviceStatus = data[0].lower()

            sql_query = """
                SELECT *, r.houseId FROM servicerequest as sr
                JOIN reservation AS r
                ON sr.reservationId = r.reservationId
                WHERE sr.serviceStatus = %s
            """

            cur.execute(sql_query, (serviceStatus,))
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = [dict(zip(column_names, row)) for row in result] if column_names and result else []
            cur.close()
            return result_dict
        
    def insert_data(self, query_type, data):
        cur = self.mysql.connection.cursor()

        try:
            if query_type == 'REGISTER_USER':
                fullname = data[0]
                userEmail = data[1]
                userPassword = data[2]
                userImage = data[3]
                phoneNumber = data[4]
                country = data[5]
                sql_query = """
                    INSERT INTO users (userFullName, userEmail, userPassword, userImage, phoneNumber, userCountry) VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql_query, (fullname, userEmail, userPassword, userImage, phoneNumber, country,))
                self.mysql.connection.commit()
                cur.close()
                return True

            if query_type == 'ADD_HOUSE':
                houseName = data[0]
                houseCategory = data[1]
                houseDescription = data[2]
                houseThumbnail = data[3]
                houseBed = data[4]
                housePeople = data[5]
                housePrice = data[6]
            
                sql_query = """
                INSERT INTO house 
                (houseName, houseCategory, houseDescription, houseThumbnail, houseBed, housePeople, housePrice) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql_query, (houseName, houseCategory, houseDescription, houseThumbnail, houseBed, housePeople, housePrice,))
                self.mysql.connection.commit()
                last_inserted_id = cur.lastrowid
                cur.close()
                return last_inserted_id
                        
            if query_type == 'ADD_HOUSE_FACILITY':
                houseId = data[0]
                houseFacility = data[1]
                sql_query = """
                    INSERT INTO housefacilities (facName, houseId) VALUES (%s, %s)
                """
                for faci in houseFacility:
                    cur.execute(sql_query, (faci, houseId,))
                    self.mysql.connection.commit()

                cur.close()
                return True
            
            if query_type == 'ADD_HOUSE_IMAGES':
                houseId = data[0]
                houseImages = data[1]
                sql_query = """
                    INSERT INTO houseimages (houseId, images) VALUES (%s, %s)
                """
                for image in houseImages:
                    cur.execute(sql_query, (houseId, image,))
                    self.mysql.connection.commit()

                cur.close()
                return True
            
            if query_type == 'ADD_HOUSE_LOCATION':
                houseId = data[0]
                houseLocation = data[1]
                houseAddress = data[2]


                sql_query = """
                    INSERT INTO houselocation (houseId, houseLocation, houseAddress) VALUES (%s, %s, %s)
                """
                cur.execute(sql_query, (houseId, houseLocation, houseAddress))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'ADD_REVIEW':
                userId = data[0]
                houseId = data[1]
                reviewNote = data[2]
                rate = data[3]
                
                sql_query = """
                    INSERT INTO userreview (userId, houseId, reviewNote, rate) VALUES (%s, %s, %s, %s)
                """
                cur.execute(sql_query, (userId, houseId, reviewNote, rate))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'ADD_RESERVATION':
                userId = data[0]
                houseId = data[1]
                bookFrom = data[2]
                booTo = data[3]
                
                sql_query = """
                    INSERT INTO reservation (userId, houseId, bookStartDate, bookEndDate) VALUES (%s, %s, %s, %s)
                """
                cur.execute(sql_query, (userId, houseId, bookFrom, booTo))
                self.mysql.connection.commit()
                cur.close()
                return True

            if query_type == 'ADD_FAVOURITE':
                userId = data[0]
                houseId = data[1]
                sql_query = """
                    INSERT INTO userfavourite (userId, houseId) VALUES (%s, %s)
                """
                cur.execute(sql_query, (userId, houseId,))
                self.mysql.connection.commit()

                cur.close()
                return True
            
            if query_type == 'INSERT_RESERVATION':
                userId = data[0]
                houseId = data[1]
                bookStartDate = data[2]
                bookEndDate = data[3]
                totalAmount = data[4]
                adultNumber = data[5]
                childrenNumber = data[6]
                bookingNote = data[7]
                reservationId = shortuuid.ShortUUID().random(length=12).upper() 
                sql_query = """
                    INSERT INTO reservation (userId, houseId, bookStartDate, bookEndDate, totalAmount, adultNumber, childrenNumber, bookingNote, reservationId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cur.execute(sql_query, (userId, houseId, bookStartDate, bookEndDate, totalAmount, adultNumber, childrenNumber, bookingNote, reservationId,)) 
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'INSERT_SERVICE_REQUEST':
                userId = data[0]
                serviceNote = data[1]
                reservationId = data[2]
                serviceId = shortuuid.ShortUUID().random(length=10).upper() 
                sql_query = """
                    INSERT INTO servicerequest (userId, reservationId, userServiceNote, serviceId) VALUES (%s, %s, %s, %s)
                """

                cur.execute(sql_query, (userId, reservationId, serviceNote, serviceId,)) 
                self.mysql.connection.commit()
                cur.close()
                return True
        
            if query_type == 'INSERT_FEEDBACK':
                userId = data[0]
                houseId = data[1]
                feedbackNote = data[2]
                houseRating = data[3]
               
                sql_query = """
                    INSERT INTO userreview (userId, houseId, reviewNote, rate) VALUES (%s, %s, %s, %s)
                """

                cur.execute(sql_query, (userId, houseId, feedbackNote, houseRating,)) 
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'INSERT_POLICY':
                policyNote = data[0]

                sql_query = """
                    INSERT INTO policy (policyNote) VALUES (%s)
                """
                cur.execute(sql_query, (policyNote,))
                self.mysql.connection.commit()
                cur.close()
                return True
            

        except Exception as e:
            print(e)
            return False

      
    def update_data(self, query_type, data):
        cur = self.mysql.connection.cursor()

        try:
            if query_type == 'UPDATE_USER':
                print(data)
                userId = data[0]
                fullname = data[1]
                phoneNumber = data[2]
                userImage = data[3]
                userEmail = data[4]

                sql_query = """
                    UPDATE users SET userFullName = %s, userEmail = %s, userImage = %s, phoneNumber = %s WHERE userId = %s
                """
                cur.execute(sql_query, (fullname, userEmail, userImage, phoneNumber, userId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'UPDATE_USER_WITHOUT_IMAGE':
                userId = data[0]
                fullname = data[1]
                phoneNumber = data[2]
                userEmail = data[3]

                sql_query = """
                    UPDATE users SET userFullName = %s, userEmail = %s, phoneNumber = %s WHERE userId = %s
                """
                cur.execute(sql_query, (fullname, userEmail, phoneNumber, userId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'UPDATE_PASSWORD':
                userId = data[0]
                userPassword = data[1]

                sql_query = """
                    UPDATE users SET userPassword = %s WHERE userId = %s
                """
                cur.execute(sql_query, (userPassword, userId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'UPDATE_CHECK_USER_STATUS':
                bookId = data[0]
                checkStatus = data[1]

                sql_query = """
                    UPDATE reservation SET bookHouseStatus = %s WHERE reservationId = %s
                """

                cur.execute(sql_query, (checkStatus, bookId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'UPDATE_BOOK_STATUS':
                bookId = data[0]
                bookStatus = data[1]

                sql_query = """
                    UPDATE reservation SET bookStatus = %s WHERE reservationId = %s
                """

                cur.execute(sql_query, (bookStatus, bookId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'UPDATE_SERVICE_REQUEST':
                serviceId = data[0]
                adminServiceNote = data[1]
                serviceStatus = 'Completed'

                sql_query = """
                    UPDATE servicerequest SET adminServiceNote = %s, serviceStatus = %s WHERE serviceId = %s
                """

                cur.execute(sql_query, (adminServiceNote, serviceStatus, serviceId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'UPDATE_HOUSE_PRICE':
                houseId = data[0]
                housePrice = data[1]

                sql_query = """
                    UPDATE house SET housePrice = %s WHERE houseId = %s
                """

                cur.execute(sql_query, (housePrice, houseId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            

        except Exception as e:
            print(e)
            return False

    def delete_data(self, query_type, data):
        cur = self.mysql.connection.cursor()

        try:
            if query_type == 'REMOVE_FAVOURITE':
                userId = data[0]
                houseId = data[1]
                sql_query = """
                    DELETE FROM userfavourite WHERE userId = %s AND houseId = %s
                """
                cur.execute(sql_query, (userId, houseId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'REMOVE_RESERVATION':
                reservationId = data[0]
                sql_query = """
                    DELETE FROM reservation WHERE reservationId = %s
                """
                cur.execute(sql_query, (reservationId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'REMOVE_RESERVATON':
                reservationId = data[0]
                sql_query = """
                    DELETE FROM reservation WHERE reservationId = %s
                """
                cur.execute(sql_query, (reservationId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'REMOVE_SERVICE_REQUEST':
                serviceId = data[0]
                sql_query = """
                    DELETE FROM servicerequest WHERE reservationId  = %s
                """
                cur.execute(sql_query, (serviceId,))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            if query_type == 'REMOVE_HOUSE':
                houseId = data[0]

                # Delete from housefacilities
                sql_query = "DELETE FROM housefacilities WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                # Delete from houseimages
                sql_query = "DELETE FROM houseimages WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                # Delete from houselocation
                sql_query = "DELETE FROM houselocation WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                # Delete from rating
                sql_query = "DELETE FROM rating WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                  # Delete from servicerequest
                sql_query = """
                    DELETE servicerequest FROM servicerequest
                    INNER JOIN reservation ON servicerequest.reservationId = reservation.reservationId
                    WHERE reservation.houseId = %s
                """
                cur.execute(sql_query, (houseId,))

                # Delete from reservation
                sql_query = "DELETE FROM reservation WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                # Delete from userfavourite
                sql_query = "DELETE FROM userfavourite WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                # Delete from userreview
                sql_query = "DELETE FROM userreview WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                # Delete from house
                sql_query = "DELETE FROM house WHERE houseId = %s"
                cur.execute(sql_query, (houseId,))

                self.mysql.connection.commit()
                cur.close()
                return True
            
        except Exception as e:
            print(e)
            return False

   
   
   