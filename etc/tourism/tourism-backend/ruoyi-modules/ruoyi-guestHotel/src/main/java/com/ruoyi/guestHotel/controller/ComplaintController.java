package com.ruoyi.guestHotel.controller;

import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.guestHotel.domain.Complaints;
import com.ruoyi.guestHotel.domain.StarhotelReviews;
import com.ruoyi.guestHotel.domain.StarhotelRooms;
import com.ruoyi.guestHotel.domain.Starhotels;
import com.ruoyi.guestHotel.domain.VO.StarhotelReviewsVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.guestHotel.service.IComplaintsService;

import java.util.ArrayList;
import java.util.List;

import static com.ruoyi.common.core.utils.PageUtils.startPage;
import static com.ruoyi.common.core.web.domain.AjaxResult.success;

@RestController
@RequestMapping("/guest/complaint")

public class ComplaintController {
    @Autowired
    private IComplaintsService complaintsService;
    /**
     * 获取投诉信息详细信息
     */
    @GetMapping(value = "/{id}")
    public List<Complaints> getInfo(@PathVariable("id") Long id)
    {
        startPage();
        List<Complaints> list_reviews= complaintsService.selectComplaintsById(id);
        return list_reviews;
    }
}
