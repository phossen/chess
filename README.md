# TODO

* Code Todo's
* Add en passant
    * Only possible for pawns
    * Only possible directly after enemy pawn moved two positions
* Add castling
    [ ] King has not moved
    [ ] Rook has not moved (and is not a Pawn-Rook)
    [ ] No piece between the rook and the king
    [ ] No position that the king goes over is threatend
    [ ] The king is not checked before and after castling
* Check draw
    * When the player on the move has no legal move available, but his king is not in check (stalemate).
    * When a position has arisen in which neither player can mate the opponent's king with any sequence of regular moves. Such a position is called a "dead position".
    * If an identical position with the same moves and the same player on the move has arisen or is about to arise on the chessboard for at least the third time and the player on the move claims it.
    * If, analogous to the previous two rules, no pawn has been moved nor a piece captured in a game for 75 moves, or the same position has arisen five times.
* Add universal chess engine interface and chess engine
* Testing
* Review&Refactoring&Documentation
* Write README
