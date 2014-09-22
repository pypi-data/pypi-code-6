import transactions
import addresses
dest_array=[]
dest_array.append(addresses.generate_publicaddress("AssemblyMade"))
dest_array.append(addresses.generate_publicaddress("AssemblyWrought"))
dest_array.append(addresses.generate_publicaddress("AssemblyForged"))
coloramt_array=[5,4,3]
#a=transactions.transfer_tx_multiple("16ucRhebuqcoDngLoZNwz2d6TjtNnLunKE", dest_array, 0.00005, "5Kh746BqkX8xTspPRAoJLYzMLe6gKp2tHeG7nk34XeS1Wjfrs1a", "16ucRhebuqcoDngLoZNwz2d6TjtNnLunKE", coloramt_array, "")
a=transactions.multiple_transfer_txs("16ucRhebuqcoDngLoZNwz2d6TjtNnLunKE", dest_array, 0.0001, "5Kh746BqkX8xTspPRAoJLYzMLe6gKp2tHeG7nk34XeS1Wjfrs1a", "16ucRhebuqcoDngLoZNwz2d6TjtNnLunKE", coloramt_array)
