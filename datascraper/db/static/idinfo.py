import sys
sys.dont_write_bytecode = True

groupings = {
    '2015 MLB Tickets': {'id': 81, 'url': 'mlb-tickets'},
    '2015 MLB Regular Season Tickets': {'id': 115753, 'url':'regular-season-mlb-tickets'},
    '2015 NFL Tickets': {'id': 121, 'url': 'nfl-tickets'},
    '2015 NFL Regular Season Tickets': {'id': 80916, 'url':'regular-season-nfl-tickets'},

}

venuesMLB = {
    'Arizona Diamondbacks': {'id': 701, 'venue': 'Chase Field', 'venueId':365},
    'Atlanda Braves': {'id': 5643, 'venue': 'Turner Field', 'venueId': 4210},
    'Baltimore Orioles': {'id': 4962, 'venue': 'Oriole Park at Camden Yards', 'venueId': 3401},
    'Boston Red Sox': {'id': 4322, 'venue': 'Fenway Park', 'venueId': 2901},
    'Chicago cubs': {'id': 5644, 'venue': 'Wrigley Field', 'venueId': 4207},

    'Chicago White Sox': {'id': 5645, 'venue': 'US Cellular Field', 'venueId': 4208},
    'Cincinnati Reds': {'id': 4862, 'venue': 'Great Ametical Ball Park', 'venueId': 5844},
    'Cleveland Indians': {'id': 4882, 'venue': 'Progressive Field', 'venueId': 3262},
    'Colorado Rockies': {'id': 5646, 'venue': 'Coors Field', 'venueId': 4205},
    'Detroit Tigers': {'id': 4182, 'venue': 'Comerica Park', 'venueId': 2741},

    'Houston Astros': {'id': 4782, 'venue': 'Minute Maid Park', 'venueId': 3221},
    'Kansas City Royals': {'id': 5647, 'venue': 'Kauffman Stadium', 'venueId': 4221},
    'Los Angeles Angels': {'id': 1062, 'venue': 'Angel Stadium', 'venueId': 9763},
    'Los Angeles Dodgers': {'id': 1061, 'venue': 'Dodger Stadium', 'venueId': 744},
    'Miami Marlins': {'id': 4342, 'venue': 'Marlins Park', 'venueId': 194876},

    'Milwaukee Brewers': {'id': 5164,'venue': 'Miller Park', 'venueId': 3626},
    'Minnesota Twins': {'id': 5648, 'venue': 'Target Field', 'venueId': 141505},
    'New York Mets': {'id': 5649, 'venue': 'Citi Field', 'venueId': 139704},
    'New York Yankees': {'id': 5950, 'venue': 'Yankee Stadium', 'venueId': 4222},
    'Oakland Athletics': {'id': 198, 'venue': 'O.co Coliseum', 'venueId': 83},

    'Philadelphia Phillies': {'id': 4344, 'venue': 'Citizens Bank Park', 'venueId': 9563},
    'Pittsburgh Pirates': {'id': 4802, 'venue': 'PNC Park', 'venueId': 3241},
    'San Diego Padres': {'id': 581, 'venue': 'Petco Park', 'venueId': 9643},
    'San Francisco Giants': {'id': 197, 'venue': 'AT&T Park', 'venueId': 82},
    'Seattle Mariners': {'id': 1043, 'venue': 'Safeco Field', 'venueId': 763},

    'St. Louis Cardinals': {'id': 5651, 'venue': 'Busch Stadium', 'venueId': 4161},
    'Tampa Bay Rays': {'id': 5652, 'venue': 'Tropicana Field', 'venueId': 4211},
    'Texas Rangers': {'id': 4343, 'venue': 'Globe Life Park', 'venueId': 2921},
    'Toronto Blue Jays': {'id': 7548, 'venue': 'Rogers Centre', 'venueId': 5882},
    'Washington Nationals': {'id': 7547, 'venue': 'Nationals Park', 'venueId': 108502},
}

venuesNFL = {
    'Kansas City Chiefs': {'id': 6063, 'venue': 'Arrowhead Stadium', 'venueId': 4467},
    'Dallas Cowboys': {'id': 6047, 'venue': 'AT&T Stadium', 'venueId': 4468},
    'Carolina Panthers': {'id': 6046, 'venue': 'Bank of America Stadium', 'venueId': 4464},
    'Seattle Seahawks': {'id': 1945, 'venue': 'CenturyLink Field', 'venueId': 4402},

    'St. Louis Rams': {'id': 6183, 'venue': 'Edward Jones Dome', 'venueId': 4621},
    'Jacksonville Jaguars': {'id': 6144, 'venue': 'EverBank Field', 'venueId': 4603},
    'Washington Redskins': {'id': 6162, 'venue': 'FedEx Field', 'venueId': 3423},
    'Cleveland Browns': {'id': 6052, 'venue': 'FirstEnergy Stadium', 'venueId': 4465},

    'Detroit Lions': {'id': 6048, 'venue': 'Ford Field', 'venueId': 3882},
    'Atlanta Falcons': {'id': 6044, 'venue': 'Georgia Dome', 'venueId': 941},
    'New England Patriots': {'id': 3582, 'venue': 'Gillette Stadium', 'venueId': 3881},
    'Pittsburgh Steelers': {'id': 5742, 'venue': 'Heinz Field', 'venueId': 4401},

    'Green Bay Packers': {'id': 6186, 'venue': 'Lambeau Field', 'venueId': 4622},
    'San Francisco 49ers': {'id': 199, 'venue': 'Levi\'s Stadium', 'venueId': 216052},
    'Philadelphia Eagles': {'id': 761, 'venue': 'Lincoln Financial Field', 'venueId': 5723},
    'Tennessee Titans': {'id': 6062, 'venue': 'Nissan Stadium', 'venueId': 8869},

    'Indianapolis Colts': {'id': 6142, 'venue': 'Lucas Oil Stadium', 'venueId': 113502},
    'Baltimore Ravens': {'id': 5962, 'venue': 'M&T Bank Stadium', 'venueId': 4461},
    'New York Giants': {'id': 6184, 'venue': 'MetLife Stadium', 'venueId': 174027},
    'New York Jets': {'id': 6143, 'venue': 'MetLife Stadium', 'venueId': 174027},

    'Minnesota Vikings': {'id': 6064, 'venue': 'TCF Bank Stadium', 'venueId': 141504},
    'Houston Texans': {'id': 6049, 'venue': 'NRG Stadium', 'venueId': 3981},
    'Oakland Raiders': {'id': 139, 'venue': 'O.co Coliseum', 'venueId': 83},
    'Cincinnati Bengals': {'id': 6045, 'venue': 'Paul Brown Stadium', 'venueId': 4463},

    'San Diego Chargers': {'id': 2124, 'venue': 'Qualcomm Stadium', 'venueId': 402},
    'Buffalo Bills': {'id': 6043, 'venue': 'Ralph Wilson Stadium', 'venueId': 4462},
    'Tampa Bay Buccaneers': {'id': 6182, 'venue': 'Raymond James Stadium', 'venueId': 405},
    'Chicago Bears': {'id': 6051, 'venue': 'Soldier Field', 'venueId': 6544},

    'Denver Broncos': {'id': 6050, 'venue': 'Sports Authority Field at Mile High', 'venueId': 4602},
    'Miami Dolphins': {'id': 3583, 'venue': 'Sun Life Stadium', 'venueId': 2566},
    'New Orleans Saints': {'id': 6065, 'venue': 'Mercedes-Benz Superdome', 'venueId': 243},
    'Arizona Cardinals': {'id': 329, 'venue': 'University of Phoenix Stadium', 'venueId': 60682},

}

venues = venuesMLB.copy()
venues.update(venuesNFL)

teamsMLB = venuesMLB.keys()
teamsNFL = venuesNFL.keys()
teams = venues.keys()