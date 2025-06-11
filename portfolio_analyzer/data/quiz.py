
quiz=[ 

    {
        'question':'What is the probability of rolling a sum greater than 4 when rolling two fair dice?', 
        'choices': ['11/12','8/9', '5/6'], 
        'answer':'5/6',
        'explanation':'Simple space=6x6(6 outcomes for each die)=36. Favorable outcomes=(1,2),(2,1),(1,3),(3,1),(1,1),(2,2)=6. P(≤4)=6/36=1/6. '\
        'Therefore P(>4)=1-P(≤4)=1-1/6=5/6=83(3)%'
    },

    {
        'question':'What insight does CAPM provide?',
        'choices': ['Risk adjusted return','Extra return for extra risk', 'Index fair value'],
        'answer':'Extra return for extra risk',
        'explanation':'CAMP is a very simple yet powerful model. It suggests that investors should expect higher returns for stocks with greater exposure to market-wide fluctuations, '\
        'as indicated by their beta. This insight helps investors understand the expected return for a given level of risk and can be used to evaluate if an investment is fairly priced.'
    },

    {
        'question':'Which of the following is NOT an assumption of the Black-Scholes option pricing model?', 
        'choices': ['No dividends are paid', 'Risk-free rate is constant', 'Markets are inefficient'], 
        'answer':'Markets are inefficient', 
        'explanation':'BSM indeed operates under flawed assumptions and more rigorous and complex models have been developed to address them'
    },

    {
        'question':'According to put-call parity, what is the relationship between a European call (C), put (P), strike price (K), and stock price (S)?', 
        'choices': ['C-P=S-K', 'C-P=S-Ke^(-rT)', 'C+P=S+K'], 
        'answer':'C-P=S-Ke^(-rT)', 
        'explanation':'Put-Call Parity is a fundamental principle in option theory. This principle requires that puts and calls have the same strike, same expiration and have the same underlying futures contract. '\
        'Thus, establishing a direct relationship between puts and calls accounting for the time value of money'
    },

    {
        'question':'In risk-neutral valuation, options are priced assuming:', 
        'choices': ['All assets earn risk-free rate', 'Investors are risk-seeking', 'Volatility is zero'], 
        'answer':'All assets earn risk-free rate', 
        'explanation':'Risk-neutral valuation is a method used in financial derivatives pricing that assumes all assets grow at the risk-free rate and are discounted using the same risk-free rate.'
    },

    {
        'question':'Which of the Treasuries is considered the longest term and has the greatest coupon value in healthy economies?', 
        'choices': ['Treasury Notes', 'Treasury Bills', 'Treasury Bonds'], 
        'answer':'Treasury Bonds', 
        'explanation':'Treasury bonds generally offer a higher return compared to Treasury notes and bills primarily due to their longer maturity periods. However in unhealthy economies could be the the opposite'
    },

    {
        'question':'According to the Capital Asset Pricing Model (CAPM), the expected return of a stock depends on:', 
        'choices': ['Total risk', 'Systematic risk', 'Firm-specific risk'], 
        'answer':'Systematic risk', 
        'explanation':'CAPM focuses on systematic (also known as market or non-diversifiable) risk, which is risk that cannot be eliminated through diversification. And sereves as the basepoint for the calculations'
    },

    {
        'question':'If the market price of a call option increases while all other parameters stay the same, implied volatility:', 
        'choices': ['Increases', 'Decreases', 'Stays the same'], 
        'answer':'Increases', 
        'explanation':'Implied volatility represents the market\'s expectation of future price fluctuations in the underlying asset, and as those expectations rise (meaning the market anticipates greater price swings), option premiums, including those on call options, tend to increase. '
    },

    {
        'question':'Forward price of an asset is equal to the futures price under what assumption:',
        'choices': ['Stochastic interest rates', 'Constant interest rates', 'American-style contract'],
        'answer':'Constant interest rates', 
        'explanation':'If interest rates are constant, the net cost of carrying an asset to maturity is the same for both futures and forward contracts, leading to equal prices.'
    },

    {
        'question':'The Sharpe ratio measures:', 
        'choices': ['Total return/volatility', 'Return per unit of risk', 'Market-relative alpha'], 
        'answer':'Return per unit of risk', 
        'explanation':'Developed by William Sharpe in the 60s, sharpe ratio is used to measure risk adjusted return, indicating how much reward an investor receives for the amount of risk they taken'
    },

    {
        'question': 'How many ways are there to fill out a March Madness bracket?',
        'choices': ['2^64', '2^63', '63^2'],
        'answer': '2^63',
        'explanation': 'There are 63 total games played (not that hard to count). For each game you have a binary choice for which teams you think will win. '\
        'You get to choose 63 times: once for each game. Thus, 2^63 (By the Fundamental Principle of Counting in case you were wondering).'
    },

    {
        'question': 'How many positive integers <1 billion have exactly three 7\'s (ex: 033 424 777)?',
        'choices': ['7777', '777', '44 641 044'],
        'answer': '44 641 044',
        'explanation': 'You got it) This is a typical "stars and bars" problem. You choose where the 7\'s go with 9 choose 3, then the other 6 spots have a choise between numbers '\
        '0-9 except for 7, that leaves us with 9 options per spot. Since we have 6 such spots we count them with 9^6. So the final answer is (9 choose 3)x9^6 = 44 641 044.'
    },

    {
        'question': 'How many bit strings are there of length 12 that have at least one 1?',
        'choices': ['4095', '3095', '5095'],
        'answer': '4095',
        'explanation': 'Every bit in a bit string has 2 choices 0 or 1. That results in 2^12 possibilities. Notice that there is only one possinle bit string with no 1\'s: '\
        'a bit string of all zeros. So, 2^12-1 bit strings will contain at least a signle 1 = 4095.'
    },

    {
        'question': 'How many 5-letter strings can be made from A, B, and C if repetition is allowed?',
        'choices': ['3^5', '5^3', '5!'],
        'answer': '3^5',
        'explanation': 'There are 5 positions that need to be filled out using one out of the three options (A,B,C). So, we need to choose one out of the three letters five times. '\
        'That gets us 3^5.'
    },

    {
        'question': 'What is the expected value when rolling a fair twelve-sided die?',
        'choices': ['12', '6', '6.5'],
        'answer': '6.5',
        'explanation': 'We need to add up all the possible outcomes of X (1+2+...+12) and divide by the number of possible outcomes. So, E(X) = 78/12 = 6.5'
    },

    {
        'question': 'Which of the following reduces the present value of future cash flows?',
        'choices': ['Lower discount rate', 'Longer time horizon', 'More frequent payments'],
        'answer': 'Longer time horizon',
        'explanation': 'The longer you wait to recieve money, the less it is worth today due to discounting.'
    },

    {
        'question': 'Which financial statement shows a firm\'s revenues and expenses?',
        'choices': ['Balance sheet', 'Cash flow statement', 'Income statement'],
        'answer': 'Income statement',
        'explanation': 'The income statement reports revenues, expenses, and profits over a period of time.'
    },

    {
        'question': 'If interest rates rise, what typically happens to bond prices?',
        'choices': ['Increase', 'Decrease', 'Remain unchanged'],
        'answer': 'Decrease',
        'explanation': 'The bond prices would decrese because investors would require a higher return due to increased interest rates, therefore the bond prices would decrese '\
        'and result in a higher yeild which would compensate for higher rates.'
    },

    {
        'question': 'Which of these increases a firm\'s return on equity (ROE), assuming net income stays the same?',
        'choices': ['Going public', 'Increasing debt', 'Decreasing margins'],
        'answer': 'Increasing debt',
        'explanation': 'By borrowing money, firms decrease their valuation, thus reducing equity. And equity is the denominator in the ROE calculation (Income/Equity). '\
        'And smaller denominator means higher output.'
    },

    {
        'question': 'You have a 10x10 cube made out of individual clear unit cubes. If you dip the entire cube in paint, how many individual cubes did not touch any paint?',
        'choices': ['60', '512', '312'],
        'answer': '512',
        'explanation': 'One uncool way to do it is to actually count such cubes which is not that difficult, just make sure to not double count. '\
        'The other "cool" way to do it is to realize if you take off the outer layer of the cube you are left off with a 8x8 cube that is still clear, and 8^3=512'
    },

    {
        'question': 'What is the probability of drawing 4 of a kind from a standard 5-card hand?',
        'choices': ['0.024', '0.01', '0.042'],
        'answer': '0.024',
        'explanation': 'The general approach to solving this kind of problems is using combinations. There are 13 kinds to choose 1 from, that is 13C1, then we need to choose all 4 suits '\
        'using 4C4. That fills 4 out of 5 "spots". Choose the last card with 48C1. So, P(X) = (13C1 x 4C4 x 48C1)/52C5'
    },

    {
        'question': 'You roll two dice and select the one with the highest roll. What is the expected value of the die you selected?',
        'choices': ['232/43', '130/97', '161/36'],
        'answer': '161/36',
        'explanation': 'Solved using recursion. Starting with max=1, for that both rolls need to be 1s, and there is only one way to do that resulting in 1/36. For max=2, either both 2s or '\
        'one of them is a 1, resulting in 3 ways = 3/36. For max=3, we have 9-3-1/36=5/36. A pattern emerges: the numerator of max=n is n^2-(the sum of all previous numerators). So (max=4)=7/36, '\
        '(max=5)=9/36, (max=6)=11/36. The expected value is the sum of the probabilities times their respective maxes.'
    },

    {
        'question': 'Suppose that two integers a and b are uniformly at random selected from S = {-10, -9, ..., 9, 10}. What is the probability that max(0,a)=min(0,b)',
        'choices': ['144/316', '121/441', '24/33'],
        'answer': '121/441',
        'explanation': 'There are a total number of pairs is 21^2=441. Max(0,a)=0 if a≤0, min(0,b)=0 if b≥0. Max(0,a)=min(0,b) if both are 0. '\
        'This happens when a≤0 and b≥0. There are 11 values for each case, thus 11^2. So, A: 121/441'
    },

    {
        'question': 'You have 10 ice cream toppings to choose from. How many different combinations ≥1 of ice cream can you create with the 10 toppings?',
        'choices': ['2^10', '2^10-1', '2^11'],
        'answer': '2^10-1',
        'explanation': 'The best way to solve it is using the bit-string way. That is you can either include or excule each toping which is a binary choice that you need to make 10 times. '\
        'It results in 2^10 less one for the case where you do not choose any which is now allowed'
    },

    {
        'question': 'You place three dots along the edges of an octagon at random. What is the probability that all three dots lie on distinct edges of the octagon?',
        'choices': ['17/36', '21/32', '25/32'],
        'answer': '21/32',
        'explanation': 'Consider the picks individually. The first dot can go to any of the 8 edges, so 8/8. The second dot can go to any edge except for the one first dot went, so 7/8 '\
        'The third one can go to any less where first and second went, so 6/8. So, P(X) = 8/8 x 7/8 x 6/8 = 21/32.'
    },
    
    {
        'question': 'If the close price of XYZ at expiration is $25, what is a $22.50 strike call worth?',
        'choices': ['$2.50', '$1.50', '$0.00'],
        'answer': '$2.50',
        'explanation': 'Simply $25.00 - $22.50 = $2.50. Because the price of an option at expiration is equal to its intrinsic value which is the difference between the price at expiration and '\
        'the strike price, or 0 in case the difference is negative.'
    },

    {
        'question': ' If the close price of ABC at expiration is $55, what is a $44.30 strike put worth?',
        'choices': ['$0', '$5.70', '$5.00'],
        'answer': '$0',
        'explanation': 'The worth of a put option at expiration is equal to its intrinsic value which is the the strike price - the close price, or 0 in case the difference is negative which '\
        'is our case.'
    },

    {
        'question': 'You have $100M to invest into companies A,B,C,D,F in increments of $1M. In how many ways can you do so?',
        'choices': ['Too many', '>sand grains on Earth', '999!'],
        'answer': 'Too many',
        'explanation': 'This is a typical "stars and bars" problem, where we have 4 bars that would separate the 5 companies and 75 stars to spare (each start is $1M). Following the formula, '\
        'the number of ways to arrange the start is 104 choose 4 which is a mind blowing number.'
    },

    {
        'question': 'We have 4 positive integers A, B, C, and D. We know AB = 16, BC = 14, and CD = 63. What is A + B + C + D?',
        'choices': ['26', '15', '33'],
        'answer': '26',
        'explanation': 'Solve using elimination. Given AB=16, there are 5 possibilities for A,B: 1,16; 2,8; 4,4; 8,2; 16,1. The first and last clearly do not work, it is easy to realize given the second equation. '\
        'Neither do 16,1 or 4,4 for the same reason. We are left with 2,8 and 8,2. The first gets stopped at the second equation because 8C cannot equal 14 given C is an integer. So the asnwer is 2,8.'
    },

    {
        'question': 'If you have 30 people in a room, what is the likelihood that at least 2 of them have the same birthday?',
        'choices': ['0.7', '0.08', '0.55'],
        'answer': '0.7',
        'explanation': 'For this classical problem we usually calculate the complement. The probability that the first two people have different birthday is 365/365 x 364/365 because every consequent person has one less '\
        '"available" birthdays. Extending the patter to 30 people, we get 365x364x...336/365^30 = 0.2937. And we need the complement of that: 1-0.2937=0.7063=0.7'
    }
]